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
from django.db.models import Sum, Count
import calendar


def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def custom_server_error_view(request):
    return render(request, '500.html', status=500)

def custom_permission_denied_view(request, exception):
    return render(request, '403.html', status=403)

def custom_bad_request_view(request, exception):
    return render(request, '400.html', status=400)


# account functionalities 
#
@login_required(login_url="signin")
def home(request):
    date_now = datetime.now()
    customerss = Customers.objects.all()

    bookings = Order.objects.all().order_by('-order_date')[:10]
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

    ## sending order data weekly ===========================================

    start_of_this_week = today - timedelta(days=today.weekday())  # Start of this week (Monday)
    start_of_last_week = start_of_this_week - timedelta(weeks=1)  # Start of last week

    # Current week data
    this_week_data = Order.objects.filter(order_date__gte=start_of_this_week)\
        .aggregate(
            total_amount=Sum('total_amount'),
            order_count=Count('id')
        )

    # Last week data
    last_week_data = Order.objects.filter(order_date__gte=start_of_last_week, order_date__lt=start_of_this_week)\
        .aggregate(
            total_amount=Sum('total_amount'),
            order_count=Count('id')
        )
    ## sending order data weekly end ===========================================



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
        "total_expense_month":total_expense_month,
        "this_week": {
            "total_amount": this_week_data['total_amount'] or 0,
            "order_count": this_week_data['order_count'] or 0,
        },
        "last_week": {
            "total_amount": last_week_data['total_amount'] or 0,
            "order_count": last_week_data['order_count'] or 0,
        },
        "bookings":bookings

    }
    return render(request, "index.html",context)


# weekly chat display 

from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime, timedelta

def weekly_order_chart_data(request):
    today = datetime.now()
    start_of_this_week = today - timedelta(days=today.weekday())
    start_of_last_week = start_of_this_week - timedelta(weeks=1)

    # Calculate data for this week
    this_week_data = Order.objects.filter(order_date__gte=start_of_this_week)\
        .values('order_date__week_day')\
        .annotate(total_amount=Sum('total_amount'))

    # Calculate data for last week
    last_week_data = Order.objects.filter(order_date__gte=start_of_last_week, order_date__lt=start_of_this_week)\
        .values('order_date__week_day')\
        .annotate(total_amount=Sum('total_amount'))

    # Initialize data arrays
    weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    this_week_chart_data = [0] * 7
    last_week_chart_data = [0] * 7

    # Map data to weekday
    for entry in this_week_data:
        weekday = entry['order_date__week_day'] - 1  # Django weekday starts from 1 (Sunday)
        this_week_chart_data[weekday] = entry['total_amount']

    for entry in last_week_data:
        weekday = entry['order_date__week_day'] - 1
        last_week_chart_data[weekday] = entry['total_amount']

    return JsonResponse({
        "labels": weekdays,
        "this_week_data": this_week_chart_data,
        "last_week_data": last_week_chart_data,
    })

def income_expense_chart_json(request):
    today = datetime.now()
    start_of_this_week = today - timedelta(days=today.weekday())  # Start of this week (Monday)

    # Initialize amounts for all weekdays (0 for empty days)
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    income_data = [0] * 7
    expense_data = [0] * 7

    # Income data for this week
    income_queryset = Income.objects.filter(date__gte=start_of_this_week)\
        .values('date__week_day')\
        .annotate(total_amount=Sum('amount'))
    for entry in income_queryset:
        weekday = entry['date__week_day'] - 2  # Adjust: Monday starts at 0
        income_data[weekday] = entry['total_amount']

    # Expense data for this week
    expense_queryset = Expense.objects.filter(date__gte=start_of_this_week)\
        .values('date__week_day')\
        .annotate(total_amount=Sum('amount'))
    for entry in expense_queryset:
        weekday = entry['date__week_day'] - 2
        expense_data[weekday] = entry['total_amount']

    # Send data as JSON
    return JsonResponse({
        "weekdays": weekdays,
        "income_data": income_data,
        "expense_data": expense_data,
    })


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