from django.db import models
from finance.models import Tax


class Services(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    authority = models.CharField(max_length=100, null=True, blank=True, help_text="Authorities that regulate the service (eg: MCA, FAIC etc)")
    total_fund_from_customer = models.FloatField(default=0, help_text="Total amount collected from customer including govt fee")
    price = models.FloatField(default=0, help_text="Price of the service after deducting govt fee")
    govt_fee = models.FloatField(default=0, help_text="Government fee for the service")
    price_before_tax = models.FloatField(null=True, blank=True, default=0)
    tax_amount = models.FloatField(default=0)
    TAX_CHOICES = (
        ("Inclusive", "Inclusive"),
        ("Exclusive", "Exclusive"),
    )
    tax = models.CharField(max_length=20, choices=TAX_CHOICES, default="Inclusive")
    tax_value = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
    # Ensure the provided `total_fund_from_customer` and `govt_fee` are valid
        if self.total_fund_from_customer is not None and self.govt_fee is not None:
            # Calculate the base price (remaining after deducting govt_fee)
            self.price = max(self.total_fund_from_customer - self.govt_fee, 0)
            
            # Handle tax calculations only if tax_value is set
            if self.tax_value:
                tax_rate = self.tax_value.tax_percentage / 100
                
                if self.tax == "Exclusive":
                    # If updating, ensure tax is recalculated from price_before_tax
                    if self.price_before_tax:
                        base_price = self.price_before_tax
                    else:
                        base_price = self.price
                    
                    # Calculate tax on base_price
                    self.tax_amount = round(base_price * tax_rate, 2)
                    self.price_before_tax = round(base_price, 2)
                    self.price = round(base_price + self.tax_amount, 2)
                
                elif self.tax == "Inclusive":
                    # Calculate price_before_tax and tax amount for inclusive tax
                    self.price_before_tax = round(self.price / (1 + tax_rate), 2)
                    self.tax_amount = round(self.price - self.price_before_tax, 2)
                    
                    # Recalculate total_fund_from_customer to include tax
                    self.total_fund_from_customer = round(self.price + self.govt_fee, 2)
            else:
                # No tax case: price_before_tax equals price, and tax_amount is zero
                self.price_before_tax = round(self.price, 2)
                self.tax_amount = 0.0
        else:
            # Invalid fund or fee: reset dependent fields
            self.price = 0.0
            self.price_before_tax = 0.0
            self.tax_amount = 0.0

        # Call the parent class save method
        super(Services, self).save(*args, **kwargs)


    def __str__(self):
        return f"Service: {self.title} Authority: {self.authority}"


class Customers(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField( null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField( null=True, blank=True)
    eid_number = models.CharField(max_length=20, null=True, blank=True)
    customer_type = models.CharField(max_length=20, default="Individual",choices=(("Individual", "Individual"), ("Company", "Company")))
    date_added = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return self.name
    

from django.db import models, transaction

# First, create a model to store the last used invoice number
class InvoiceCounter(models.Model):
    last_number = models.IntegerField(default=0)
    
    class Meta:
        # Ensure we only have one counter record
        constraints = [
            models.UniqueConstraint(fields=['id'], name='singleton_counter')
        ]


class Order(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.SET_NULL,null=True,blank=True)
    invoice_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)

    total_amount_from_customer = models.FloatField(default=0)  # Set default to 0
    service_fee = models.FloatField(default=0)  # Set default to 0
    total_amount_before_discount = models.FloatField(default=0)  # Set default to 0
    total_tax = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)

    payment_status1 = models.CharField(max_length=20, default='UNPAID', choices=(("UNPAID","UNPAID"),("PAID","PAID"),("PARTIALLY","PARTIALLY")))
    payment_status = models.BooleanField(default=False)

    discount = models.FloatField(default=0)
    bill_discount = models.FloatField(default=0)

    save_status = models.BooleanField(default=False)

    paid_amount = models.FloatField(default=0)
    balance_amount = models.FloatField(default=0)

    delivery_status = models.CharField(max_length=30, default="Not Delivered", choices= (
                                                                                            ("Not Delivered", "Not Delivered"),
                                                                                            ("Partially Delivered", "Partially Delivered"),
                                                                                            ("Delivered", "Delivered"),
                                                                                            ("Cancelled", "Cancelled"),
                                                                                        ))

    def update_totals(self):
        total_amount_from_customer = 0
        service_fee = 0
        total_amount_before_discount = 0
        total_tax = 0
        total_discount = 0
        total_amount = 0

        for item in self.orderitem_set.all():
            # Sum values from all related OrderItems
            total_amount_from_customer += item.price_from_customer
            service_fee += item.service_fee
            total_amount_before_discount += item.total_price - item.discount
            total_tax += item.total_tax
            total_amount += item.total_price  # Total price includes discounts and tax

        # Apply additional bill discount
        total_discount += self.bill_discount
        total_amount -= self.bill_discount

        # Update order fields
        self.total_amount_from_customer = total_amount_from_customer - self.bill_discount
        self.service_fee = service_fee
        self.total_amount_before_discount = total_amount_before_discount
        self.total_tax = total_tax
        self.total_amount = total_amount
        self.discount = total_discount
        self.save()

    def calculate_balance(self):
        # Balance calculation remains the same...
        discounted_total = self.total_amount - self.discount
        self.balance_amount = discounted_total - self.paid_amount
        self.save()
        
    def save(self, *args, **kwargs):
        # Update balance amount before saving
        self.balance_amount = self.total_amount_from_customer - self.paid_amount
        
        # Update payment status based on payed amount
        if self.paid_amount == 0:
            self.payment_status1 = 'UNPAID'
        elif self.paid_amount >= self.total_amount_from_customer:
            self.payment_status1 = 'PAID'
        else:
            self.payment_status1 = 'PARTIALLY'
        
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.invoice_number} by {self.customer.name}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service_title = models.CharField(max_length=100, null=True, blank=True)
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, blank=True, related_name="orderitem")
    price_from_customer = models.FloatField()
    discount = models.FloatField(default=0)
    service_fee = models.FloatField(default=0)
    total_price = models.FloatField()  # Total price after discount and tax
    total_tax = models.FloatField()  # Total tax for the item
    delivery_status = models.CharField(max_length=30, default="Not Delivered", choices= (
                                                                                            ("Not Delivered", "Not Delivered"),
                                                                                            ("Partially Delivered", "Partially Delivered"),
                                                                                            ("Delivered", "Delivered"),
                                                                                            ("Cancelled", "Cancelled"),
                                                                                            
                                                                                        ))

    def save(self, *args, **kwargs):
        # self.total_price = self.total_tax - self.
        try:
            self.service_title = self.service.title
        except:
            self.service_title = "No Service"
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.service_title} - Order: {self.order}"


class OrderItemClient(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    service_order = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name="service_order_client")
    eid = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)



class OrderItemStatus(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='order_status')
    Description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

