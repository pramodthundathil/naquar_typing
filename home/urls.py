from django.urls import path
from .import views

urlpatterns = [ 

    path("home/", views.home, name="home"),
    path("", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),

    # user configuration 
    path("users_add",views.users_add,name="users_add"),
    path("add_user_form",views.add_user_form,name="add_user_form"),
    path("user_single/<int:pk>",views.user_single,name="user_single"),
    path("user_delete/<int:pk>",views.user_delete,name="user_delete"),


    #customer urls
    path("customer_list",views.customer_list,name="customer_list"),
    path("add_customer",views.add_customer,name="add_customer"),
    path("customer_single/<int:pk>", views.customer_single, name="customer_single"),
    path("delete_customer/<int:pk>", views.delete_customer, name="delete_customer"),

]