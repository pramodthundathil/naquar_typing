from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from  .decorators import unauthenticated_user

# datetime imports
from datetime import datetime

#importing forms
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser
from service.models import Order
from finance.models import Income, Expense

from django.utils import timezone
from django.db.models import Sum
import calendar





# account functionalities 
#
@login_required(login_url="signin")
def home(request):
    date_now = datetime.now()
    customerss = Customers.objects.all()
    # Get today's date
    today = timezone.now().date()

    # Filter orders for today
    today_orders = Order.objects.filter(order_date__date=today)
    # Calculate the number of bookings
    number_of_bookings = today_orders.count()
    total_amount_today = today_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0


    # Get the current year and month
    current_year = today.year
    current_month = today.month
    current_month_name = calendar.month_name[current_month]

    # Filter orders for the current month
    month_orders = Order.objects.filter(order_date__year=current_year, order_date__month=current_month)

    # Calculate the number of bookings and total amount for the current month
    number_of_bookings_month = month_orders.count()
    total_amount_month = month_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0


    today_income = Income.objects.filter(date=today)
    today_expense = Expense.objects.filter(date=today)

    # Calculate totals for today
    total_income_today = today_income.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense_today = today_expense.aggregate(Sum('amount'))['amount__sum'] or 0

    # **Income and Expense for This Month**
    # Filter this month's income and expense
    month_income = Income.objects.filter(date__year=current_year, date__month=current_month)
    month_expense = Expense.objects.filter(date__year=current_year, date__month=current_month)

    # Calculate totals for this month
    total_income_month = month_income.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense_month = month_expense.aggregate(Sum('amount'))['amount__sum'] or 0


    context = {
        "date_now": date_now,
        "customerss":customerss,
        "number_of_bookings":number_of_bookings,
        "total_amount_today":total_amount_today,
        "number_of_bookings_month":number_of_bookings_month,
        "total_amount_month":total_amount_month,
        "month":current_month_name,
        "total_income_today":total_income_today,
        "total_expense_today":total_expense_today,
        "total_income_month":total_income_month,
        "total_expense_month":total_expense_month

    }
    return render(request, "index.html",context)

@unauthenticated_user
def signin(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pswd")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            redirect("signin")
    return render(request, "login.html")


def signout(request):
    logout(request)
    return redirect("signin")

#========================================================================================================
# user functionalities
# admin creating users 

@login_required(login_url="signin")
def users_add(request):
    form = CustomUserCreationForm()
    users = CustomUser.objects.all()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect("users_add")
        else:
            messages.error(request, "User creation failed.")
            return redirect("users_add")
    context = { "form": form, "users": users}
    return render(request, "list-user.html",context)


@login_required(login_url="signin")
def add_user_form(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect("users_add")
        else:
            messages.error(request, "User creation failed.")
            return redirect("users_add")
    context = {
        "form":form
    }
    return render(request,"add-user.html",context)

@login_required(login_url="signin")
def user_single(request,pk):
    user = get_object_or_404(CustomUser, pk=pk)
    form = CustomUserChangeForm(instance = user )
    if request.method =="POST":
        form = CustomUserChangeForm(request.POST,instance = user)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request,"User data updated....")
            return redirect("users_add")


    return render(request, "user-single.html", {"user": user,"form":form})




@login_required(login_url="signin")
def user_delete(request,pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.delete()
    messages.success(request,"User Deleted Success....")
    return redirect("users_add")



#========================================================================================================
# Peoples 
# customers 
# models form service app 
#========================================================================================================

from service.forms import CustomersForm
from service.models import Customers

@login_required(login_url="signin")
def customer_list(request):
    form = CustomersForm()
    customers = Customers.objects.all()
    if request.method == 'POST':
        form = CustomersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully')
            return redirect('customer_list')
        else:
            messages.error(request, 'Service not added')
            return redirect('customer_list')
    return render(request,"list-customers.html",{'form': form,"customers":customers})


@login_required(login_url="signin")
def add_customer(request):
    form = CustomersForm()
    if request.method == 'POST':
        form = CustomersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully')
            return redirect('customer_list')
        else:
            messages.error(request, 'Service not added')
            return redirect('services')
    return render(request, 'add-customers.html', {'form': form})


@login_required(login_url="signin")
def customer_single(request, pk):
    service = get_object_or_404(Customers, pk=pk)
    orders = Order.objects.filter(customer = service)
    form = CustomersForm(instance=service)
    if request.method == "POST":
        form = CustomersForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully')
            return redirect('customer_list')
        else:
            messages.error(request, 'Service not updated')
            return redirect('customer_list')
    return render(request, 'customer-single.html', {"form":form,"service":service,"bookings":orders} )


@login_required(login_url="signin")
def delete_customer(request, pk):
    service = get_object_or_404(Customers, pk=pk)
    service.delete()
    messages.success(request, 'Customer deleted successfully')
    return redirect('customer_list')


@login_required(login_url='signin')
def settings(request):
    if request.method == "POST":
        cpswd = request.POST.get('cpswd')
        npswd = request.POST.get('npswd')
        cnpswd = request.POST.get('cnpswd')

        username = request.user.username
        user = authenticate(request, username = username, password = cpswd)
        if user is not None:
            user = request.user
            if npswd == cnpswd:
                user.set_password(npswd)
                user.save()
                messages.error(request,"Password Changed successfully. Please Login To Continue.....")
                return redirect(settings)
            else:
                messages.error(request,"Confirm password do not match")
                return redirect(settings)
        else:
            messages.error(request,"You are entered wrong password")
            return redirect(settings)
    return render(request,"settings.html")