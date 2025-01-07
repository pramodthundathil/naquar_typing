from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServicesForm
from .models import Services, Customers, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from home.models import CustomUser
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



# service order creation 
def generate_serial_number():
    with transaction.atomic():
        # Get the latest order based on ID to find the last invoice number
        last_order = Order.objects.order_by('-id').first()
        
        if last_order and last_order.invoice_number.startswith("SI-"):
            # Extract the numeric part, increment it, and format it with leading zeros
            last_number = int(last_order.invoice_number.split("-")[1])
            new_number = str(last_number + 1).zfill(5)  # Ensures it's 5 digits
        else:
            # Start from "SI-00001" if no previous order exists
            new_number = "00001"
        
        return f"SI-{new_number}"


@login_required(login_url='SignIn')
def CreateOrder(request):
    TokenU = generate_serial_number()

    order = Order.objects.create(invoice_number=TokenU)
    order.save()

    return redirect(create_booking,pk = order.id)

@login_required(login_url="signin")
def create_booking(request, pk):
    order = get_object_or_404(Order, id = pk)
    customerss = Customers.objects.values(
        "id", "name", "phone", "email", "eid_number", "address"
    ) 
    services = Services.objects.values(
       "id", "title","authority"
    )

    context = {"customerss":customerss,
               "services":services,
               "order":order
               }
    return render(request, 'create-booking.html',context)


@login_required(login_url='SignIn')
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