from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServicesForm, CustomersForm, OrderItemClientForm
from .models import Services, Customers, Order, OrderItem, OrderItemClient, OrderItemStatus, InvoiceCounter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from home.models import CustomUser
from finance.models import Income, Expense
from django.db import transaction

# Create your views here.
@login_required(login_url="signin")
def services(request):
    form = ServicesForm()
    service = Services.objects.all()
    if request.method == 'POST':
        form = ServicesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully')
            return redirect('services')
        else:
            messages.error(request, 'Service not added')
            return redirect('services')
    context = {
        'form': form,
        "service1":service
    }
    return render(request, 'services.html',context)

@login_required(login_url="signin")
def add_service(request):
    form = ServicesForm()
    if request.method == 'POST':
        form = ServicesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully')
            return redirect('services')
        else:
            messages.error(request, 'Service not added')
            return redirect('services')
    return render(request, 'add-service.html', {'form': form})


@login_required(login_url="signin")
def service_single(request, pk):
    service = get_object_or_404(Services, pk=pk)
    form = ServicesForm(instance=service)
    if request.method == "POST":
        form = ServicesForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully')
            return redirect('services')
        else:
            messages.error(request, 'Service not updated')
            return redirect('services')
    return render(request, 'service-single.html', {"form":form,"service":service} )


@login_required(login_url="signin")
def delete_service(request, pk):
    service = get_object_or_404(Services, pk=pk)
    service.delete()
    messages.success(request, 'Service deleted successfully')
    return redirect('services')



# service order creation  list order update order functions and ajax returns 

def list_bookings(request):
    context = {
        "bookings": Order.objects.all().order_by("-order_date")
    }
    return render(request,"list-bookings.html",context)

def edit_order_booking(request, pk):
    order = get_object_or_404(Order, id = pk)
    return render(request,"order_edit.html",{"order":order})

def delete_order(request,pk):
    order = get_object_or_404(Order, id = pk)
    order.delete()
    messages.success(request,"Order Deleted Success......")
    return redirect("list_bookings")

def generate_serial_number():
    with transaction.atomic():
        # Get or create the counter
        counter, created = InvoiceCounter.objects.get_or_create(
            id=1,
            defaults={'last_number': 0}
        )
        
        # Increment the counter
        counter.last_number += 1
        counter.save()
        
        # Format the new number with leading zeros
        new_number = str(counter.last_number).zfill(5)
        
        return f"SI-{new_number}"
    


@login_required(login_url='signin')
def CreateOrder(request):
    TokenU = generate_serial_number()

    order = Order.objects.create(invoice_number=TokenU)
    order.save()

    return redirect(create_booking,pk = order.id)

@login_required(login_url="signin")
def create_booking(request, pk):
    form  = CustomersForm()
    client_form  = OrderItemClientForm()
    order = get_object_or_404(Order, id = pk)
    customerss = Customers.objects.values(
        "id", "name", "phone", "email", "eid_number", "address"
    ) 
    services = Services.objects.values(
       "id", "title","authority"
    )
    context = {"customerss":customerss,
               "services":services,
               "order":order,
               "form":form,
               "client_form":client_form
               }
    return render(request, 'create-booking.html',context)


@login_required(login_url='signin')
@csrf_exempt
def add_order_item(request, pk):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        client_form = OrderItemClientForm()
        print(product_id, "))))))))))))))))))))))))))))))))))))))))))")
        
        try:
            order = Order.objects.get(id=pk)
            if order.save_status == True:
                return JsonResponse({"success": False, "error": "Cannot Be added New Item to This order"})
            
            product = Services.objects.get(id=product_id)
            
            # Create order item with base values
            order_item = OrderItem.objects.create(
                order=order, 
                service=product, 
                price_from_customer=product.total_fund_from_customer,  # This will be the base price
                service_fee=product.govt_fee,
                total_price=product.price, 
                total_tax=product.tax_amount,
                govt_fine=0,  # Default to 0, can be updated later
                extra_amount=0  # Default to 0, can be updated later
            )
            
            # The save method will handle the price calculations
            order_item.save()    
            
            # order.update_totals()  # Uncomment if you have this method
            
            # Render the order items table
            order_items_html = render_to_string('ajax/order_items_table.html', {
                'order': order,
                "client_form": client_form
            })
            return JsonResponse({"success": True, "html": order_items_html})
            
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Services.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})
    
    return JsonResponse({"success": False, "error": "Invalid request"})





@login_required(login_url='signin')
@csrf_exempt
def update_order_customer(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            customer = Customers.objects.get(id=customer_id)
            order.customer = customer
            order.save()
            customer_details_html = render_to_string('ajax/customerdetailsonpos.html', {'customers': customer,"order" : order})
            print(customer_details_html)
            return JsonResponse({"success": True, "html": customer_details_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Customers.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@csrf_exempt
def delete_order_item(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = get_object_or_404(OrderItem, id=item_id)
        order = item.order
        customer_details_html = render_to_string('ajax/order_items_table.html', {"order" : order})
        if order.save_status == True:
            return JsonResponse({"error": True,"message":"Item cannot be Deleted It a Saved item", "html": customer_details_html})
        else:
            item.delete()
            # customer_details_html = render_to_string('ajax/order_items_table.html', {"order" : order})
            # print(customer_details_html)
            return JsonResponse({"success": True,"message":"Item Deleted", "html": customer_details_html})
    return JsonResponse({"success": False, "message": "Invalid request."})




@csrf_exempt
def update_order_payment(request, order_id):
    if request.method == 'POST':
        paid_amount = float(request.POST.get('paid_amount'))
        # discount = float(request.POST.get('discount'))
        
        try:
            order = Order.objects.get(id=order_id)    
            order.paid_amount = paid_amount
            # order.discount = discount

            order.balance_amount = order.total_amount_from_customer - paid_amount

            
                        
            if paid_amount == 0:
                order.payment_status1 = 'UNPAID'
            elif paid_amount >= order.total_amount_from_customer:
                order.payment_status1 = 'PAID'
            else:
                order.payment_status1 = 'PARTIALLY'
                
            order.save()
            order.update_totals()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url='signin')
@csrf_exempt 
def add_discount(request, pk):
    order = get_object_or_404(Order, id =pk)
    if request.method == "POST":
        discount =float(request.POST.get('discount'))
        order.bill_discount = discount
        order.save()
        order.update_totals()
        messages.info(request,"discount added...")
        return redirect(create_booking, pk = pk)
    

@login_required(login_url='signin')
@csrf_exempt 
def add_fine_to_order_item(request, pk):
    order_item = get_object_or_404(OrderItem, id =pk)
    if request.method == "POST":
        fine =float(request.POST.get('fine'))
        order_item.govt_fine = fine
        order_item.save()
        order_item.order.update_totals()
        messages.info(request,"Fine added...")
        return redirect(create_booking, pk = order_item.order.pk)
    

@login_required(login_url='signin')
@csrf_exempt 
def add_extras_to_order_item(request, pk):
    order_item = get_object_or_404(OrderItem, id =pk)
    if request.method == "POST":
        fine =float(request.POST.get('extra'))
        order_item.extra_amount = fine
        order_item.save()
        order_item.order.update_totals()
        messages.info(request,"Extra amount added...")
        return redirect(create_booking, pk = order_item.order.pk)
    

@login_required(login_url='signin')
@csrf_exempt 
def add_payment(request, pk):
    order = Order.objects.get(id = pk)
    if request.method == "POST":
        try:
            amount = float(request.POST.get("amount"))
            payment_mode = request.POST.get("mode_payment")
            order.paid_amount += amount
            order.save()
            if amount > 0:
                expense = Income(
                        particulars = f"Amount Against order {order.invoice_number}",
                        amount =  amount,
                        bill_number = order.invoice_number,
                        payment_mode = payment_mode,
                        other = order.customer.name if order.customer else 'Cash Customer'
                    )
                
                expense.save()  
            messages.success(request,"Payment Added.....")
            return redirect(create_booking, pk = pk)
        except:
            messages.success(request,"Something Wrong.....")
            return redirect(create_booking, pk = pk)

    
    return redirect(create_booking, pk = pk)





from num2words import num2words

def amount_in_words(amount):
    # Split amount into whole and decimal parts
    whole_part = int(amount)
    decimal_part = int(round((amount - whole_part) * 100))
    
    # Convert each part to words
    whole_part_words = num2words(whole_part, lang='en')
    decimal_part_words = num2words(decimal_part, lang='en')
    
    # Combine with custom currency terms
    return f"{whole_part_words.capitalize()} Dirhams and {decimal_part_words.capitalize()} Fils Only"

def invoice(request,pk):
    order = Order.objects.get(id = pk)

    context = {
        "order":order,
        "total_in_words": amount_in_words(round(order.total_amount_from_customer,2)),
        'g_fee': float(order.total_extra) + float(order.service_fee) 
    }
    return render(request, 'invoice_template.html',context )


import qrcode
import io
from django.http import HttpResponse
from django.core.files.base import ContentFile
import base64
from django.shortcuts import render, get_object_or_404
from .models import Order

def voucher(request, pk):
    order = get_object_or_404(Order, id=pk)
    
    # Generate the QR code URL
    qr_url = request.build_absolute_uri(f"/services/create_booking/{order.id}")

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    # Convert QR code to an image
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    context = {
        "order": order,
        "total_in_words": amount_in_words(round(order.total_amount_from_customer, 2)),
        "qr_image": qr_image,  # Pass the QR code image
    }
    return render(request, 'invoice_voucher.html', context)


 

@login_required(login_url='signin')
def add_customer(request,pk):
    form  = CustomersForm()
    order = get_object_or_404(Order, id = pk)
    if request.method == "POST":
        form = CustomersForm(request.POST)
        if form.is_valid():
            customer = form.save()
            customer.save()
            order.customer = customer
            order.save()
            messages.success(request, "customer added to order.....")
            return redirect(create_booking,pk= pk )


from django.db import IntegrityError

@login_required(login_url='signin')
@csrf_exempt
def add_client_to_service(request,pk):
    order_item = get_object_or_404(OrderItem,pk = pk)
    form = OrderItemClientForm()
    if request.method == "POST":
        # try:
        form = OrderItemClientForm(request.POST)
        if form.is_valid():
            try:
                client = form.save(commit=False)
                client.service_order = order_item
                
                # Attempt to save the client object
                client.save()
                
                messages.success(request, "Client info added successfully.")
                return redirect(create_booking, pk=order_item.order.id)
            except IntegrityError:
                # Handle UNIQUE constraint violation
                messages.error(request, "This service order already has a client associated with it.")
                return redirect(create_booking, pk=order_item.order.id)
        else:
            messages.error(request, "Form is invalid. Please correct the errors.")
            return redirect(create_booking, pk=order_item.order.id)



    
@login_required(login_url='signin')
def add_client_form_edit_tab(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        eid = request.POST.get("eid")
        description = request.POST.get("dis")
        
        # Use get_or_create to fetch or create the OrderItemClient
        client, created = OrderItemClient.objects.get_or_create(
            service_order=order_item,
            defaults={'name': name, 'eid': eid, 'description': description}
        )
        
        if not created:
            # Update the existing client details if it already exists
            client.name = name
            client.eid = eid
            client.description = description
            client.save()

        messages.success(request, "Client details have been successfully added/updated.")
        return redirect(edit_order_booking, pk=order_item.order.id)
    else:
        messages.error(request, "Form submission failed. Please correct the errors.")
        return redirect(edit_order_booking, pk=order_item.order.id)


@login_required(login_url='signin')
def create_status_update(request, pk):
    order_item = get_object_or_404(OrderItem,id = pk)
    if request.method == "POST":
        description = request.POST.get("dis")
        status = OrderItemStatus.objects.create(Description = description , order_item = order_item)
        status.save()
        messages.success(request, "Item Status Updated Successfully")
        return redirect(edit_order_booking, pk=order_item.order.id)
    else:
        messages.error(request, "Form submission failed. Please correct the errors.")
        return redirect(edit_order_booking, pk=order_item.order.id)
    

@login_required(login_url='SignIn')
def save_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    previous_paid_amount = order.paid_amount
    # Save the order and calculate totals
    print(previous_paid_amount,"----------------------------------------")
    order.update_totals()
    order.calculate_balance()
    new_paidamount =  order.paid_amount - previous_paid_amount
    print(new_paidamount,"----------------------------------------")
    if Income.objects.filter(bill_number = order.invoice_number).exists():
        expense = Income.objects.filter(bill_number = order.invoice_number)
        total = 0
        
        for ex in expense:
            total = total + ex.amount
        
        amount = order.paid_amount - total
        if amount > 0:
            expense = Income(
                particulars = f"Amount Against order {order.invoice_number}",
                amount =  round(amount, 2),
                bill_number = order.invoice_number,
                other = order.customer.name if order.customer else 'Cash Customer'
            
            )
        
            expense.save() 
    else:
        if order.paid_amount > 0:
            expense = Income(
                    particulars = f"Amount Against order {order.invoice_number}",
                    amount =  order.paid_amount,
                    bill_number = order.invoice_number,
                    other = order.customer.name if order.customer else 'Cash Customer'
                
                )
            
            expense.save()   
    
    # Adjust stock
    try:
        if order.save_status == False:
            order.save_status = True
            order.save()
            return redirect(create_booking,pk = order_id)

        else:
            messages.info(request,"Cannot be save it is already saved the item")

            return redirect("create_booking",pk = order_id)
    except ValueError as e:
        messages.info(request,"Not Enough stock...")
        return redirect("create_booking",pk = order_id)


@login_required(login_url='SignIn')
def change_delivery_status(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)

    order.delivery_status = "Delivered"
    order.save()

    order_items = order.orderitem_set.all()
    order_items.update(delivery_status="Delivered")

    return redirect(edit_order_booking, pk=order_id)


@login_required(login_url='SignIn')
def change_delivery_status_to_service_item(request, order_id):
   
    order_item = get_object_or_404(OrderItem, id=order_id)
    order_item.delivery_status = "Delivered"
    order_item.save()
    all_items_delivered = order_item.order.orderitem_set.all().filter(delivery_status="Delivered").count() == order_item.order.orderitem_set.count()

    if all_items_delivered:
        order_item.order.delivery_status = "Delivered"
    else:
        order_item.order.delivery_status = "Partially Delivered"

    order_item.order.save()

    return redirect(edit_order_booking, pk=order_item.order.id)


@login_required(login_url='SignIn')
def filter_booking(request):
    orders = Order.objects.all()

    # Apply filters if present in the request
    if 'payment_status1' in request.GET and request.GET['payment_status1']:
        orders = orders.filter(payment_status1=request.GET['payment_status1'])

    if 'delivery_status' in request.GET and request.GET['delivery_status']:
        orders = orders.filter(delivery_status=request.GET['delivery_status'])

    if 'total_amount' in request.GET and request.GET['total_amount']:
        orders = orders.filter(total_amount__gte=request.GET['total_amount'])


    return render(request,"filter_for_order.html",{"orders":orders})




@csrf_exempt
def filter_booking_ajax(request):
    orders = Order.objects.all()
    if 'payment_status1' in request.GET and request.GET['payment_status1']:
        orders = orders.filter(payment_status1=request.GET['payment_status1'])

    if 'delivery_status' in request.GET and request.GET['delivery_status']:
        orders = orders.filter(delivery_status=request.GET['delivery_status'])

    if 'total_amount' in request.GET and request.GET['total_amount']:
        orders = orders.filter(total_amount_from_customer__gte=request.GET['total_amount'])
    customer_details_html = render_to_string('ajax/filter.html', {"orders" : orders})

    return JsonResponse({"success": True,"message":"order found", "html": customer_details_html})
        
       

    



