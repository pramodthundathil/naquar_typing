from django.urls import path
from . import views

urlpatterns = [ 

    path("services", views.services, name="services"),
    path("service_single/<int:pk>", views.service_single, name="service_single"),
    path("delete_service/<int:pk>", views.delete_service, name="delete_service"),
    path("add_service", views.add_service, name="add_service"),
    path("CreateOrder", views.CreateOrder, name="CreateOrder"),
    
    path("create_booking/<pk>", views.create_booking, name="create_booking"),
    path("update_order_customer",views.update_order_customer,name="update_order_customer")
]