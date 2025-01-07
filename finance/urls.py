from django.urls import path
from .import views 

urlpatterns = [
    path("AddTax/", views.AddTax, name="AddTax"),
    path("ListTax/", views.ListTax, name="ListTax"),
    path("delete_tax/<int:pk>", views.delete_tax, name="delete_tax"),
    path("tax_single_update/<int:pk>", views.tax_single_update, name="tax_single_update"),
]