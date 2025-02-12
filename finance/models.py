from django.db import models


class Tax(models.Model):
    tax_name = models.CharField(max_length=20)
    tax_percentage = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}  {} %'.format(str(self.tax_name),(self.tax_percentage))


from django.db import models

class Income(models.Model):
    date = models.DateField(auto_now_add=True)
    particulars = models.CharField(max_length=255)
    amount = models.FloatField()
    bill_number = models.CharField(max_length=20, default="No Bill")
    payment_mode = models.CharField(max_length=20, default="Cash",choices=[
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Net Banking', 'Net Banking'),
        ('UPI', 'UPI'),
        ('Cheque', 'Cheque'),
        ('Other', 'Other')
    ] )
    
    other = models.CharField(max_length=255, default=" ", null=True, blank=True)


class Expense(models.Model):
    date = models.DateField(auto_now_add=True)
    particulars = models.CharField(max_length=255)
    amount = models.FloatField()
    bill_number = models.CharField(max_length=20, default="No Bill")
    payment_mode = models.CharField(max_length=20, default="Cash",choices=[
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Net Banking', 'Net Banking'),
        ('UPI', 'UPI'),
        ('Cheque', 'Cheque'),
        ('Other', 'Other')
    ] )

    other = models.CharField(max_length=255, default=" ",null=True, blank=True)
