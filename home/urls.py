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

    path("settings",views.settings,name='settings'),
    path('weekly_order_chart_data/', views.weekly_order_chart_data, name='weekly_order_chart_data'),
    path('income_expense_chart_json/', views.income_expense_chart_json, name='income_expense_chart_json'),
]

handler404 = views.custom_page_not_found_view
handler500 = views.custom_server_error_view
handler403 = views.custom_permission_denied_view
handler400 = views.custom_bad_request_view