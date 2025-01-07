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

# account functionalities 
#
@login_required(login_url="signin")
def home(request):
    date_now = datetime.now()
    customerss = Customers.objects.all()

    context = {
        "date_now": date_now,
        "customerss":customerss
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
    return render(request, 'customer-single.html', {"form":form,"service":service} )


@login_required(login_url="signin")
def delete_customer(request, pk):
    service = get_object_or_404(Customers, pk=pk)
    service.delete()
    messages.success(request, 'Customer deleted successfully')
    return redirect('customer_list')