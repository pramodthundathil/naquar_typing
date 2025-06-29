from django.urls import path
from . import views

urlpatterns = [ 

    path("services", views.services, name="services"),
    path("service_single/<int:pk>", views.service_single, name="service_single"),
    path("delete_service/<int:pk>", views.delete_service, name="delete_service"),
    path("add_service", views.add_service, name="add_service"),
    
    path("list_bookings",views.list_bookings,name="list_bookings"),
    path("delete_order/<int:pk>",views.delete_order,name="delete_order"),
    path("CreateOrder", views.CreateOrder, name="CreateOrder"),
    path("create_booking/<pk>", views.create_booking, name="create_booking"),
    path("update_order_customer",views.update_order_customer,name="update_order_customer"),
    path('add_order_item/<int:pk>', views.add_order_item, name='add_order_item'),
    path('delete_order_item/', views.delete_order_item, name='delete_order_item'),
    path("invoice/<int:pk>",views.invoice,name="invoice"),
    path("voucher/<int:pk>",views.voucher,name="voucher"),
    path("add_customer/<int:pk>",views.add_customer,name="add_customer"),
    path("add_client_to_service/<int:pk>",views.add_client_to_service,name="add_client_to_service"),
    path("edit_order_booking/<int:pk>",views.edit_order_booking,name="edit_order_booking"),
    path("add_client_form_edit_tab/<int:pk>",views.add_client_form_edit_tab,name="add_client_form_edit_tab"),
    path("create_status_update/<int:pk>",views.create_status_update,name="create_status_update"),
    path("change_delivery_status/<int:order_id>",views.change_delivery_status,name="change_delivery_status"),
    path("change_delivery_status_to_service_item/<int:order_id>",views.change_delivery_status_to_service_item,name="change_delivery_status_to_service_item"),

    path("update_order_payment/<int:order_id>",views.update_order_payment,name="update_order_payment"),
    path("add_discount/<int:pk>",views.add_discount,name="add_discount"),
    path("add_payment/<int:pk>",views.add_payment,name="add_payment"),
    path("save_order/<int:order_id>",views.save_order,name="save_order"),

    path("add_fine_to_order_item/<int:pk>",views.add_fine_to_order_item,name="add_fine_to_order_item"),
    path("add_extras_to_order_item/<int:pk>",views.add_extras_to_order_item,name="add_extras_to_order_item"),

    path("filter_booking",views.filter_booking,name="filter_booking"),
    path("filter_booking_ajax",views.filter_booking_ajax,name="filter_booking_ajax")

]