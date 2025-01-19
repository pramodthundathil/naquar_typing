from django.urls import path
from .import views 

urlpatterns = [
    path("AddTax/", views.AddTax, name="AddTax"),
    path("ListTax/", views.ListTax, name="ListTax"),
    path("delete_tax/<int:pk>", views.delete_tax, name="delete_tax"),
    path("tax_single_update/<int:pk>", views.tax_single_update, name="tax_single_update"),

    path("income",views.income, name= "income"),
    path("expence",views.expence, name= "expence"),
    path("balance_sheet",views.balance_sheet, name= "balance_sheet"),
    path("balance_sheet_selected",views.balance_sheet_selected, name= "balance_sheet_selected"),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('delete_income/<int:pk>', views.delete_income, name='delete_income'),
    path('delete_expense/<int:pk>', views.delete_expense, name='delete_expense'),
    path('update_income/<int:pk>', views.update_income, name='update_income'),
    path('update_expense/<int:pk>', views.update_expense, name='update_expense'),
    path("tax_calculation",views.tax_calculation,name="tax_calculation"),

    

        #bulk delete

   
    path("delete_bulk_invoice",views.delete_bulk_invoice,name="delete_bulk_invoice"),
    path("delete_bulk_invoice_partial",views.delete_bulk_invoice_partial,name="delete_bulk_invoice_partial"),
    path("delete_bulk_invoice_pending",views.delete_bulk_invoice_pending,name="delete_bulk_invoice_pending"),
    path("delete_bulk_income",views.delete_bulk_income,name="delete_bulk_income"),
    path("delete_bulk_expense",views.delete_bulk_expense,name="delete_bulk_expense"),


        # reports
    path("download_db",views.download_db,name="download_db"),
    path("reports",views.reports,name="reports"),
    path('expence_report_excel/', views.expence_report_excel, name='expence_report_excel'),
    path('expence_report_pdf/', views.expence_report_pdf, name='expence_report_pdf'),
    path('income_report_excel/', views.income_report_excel, name='income_report_excel'),
    path('income_report_pdf/', views.income_report_pdf, name='income_report_pdf'),
    path('sale_report_excel/', views.sale_report_excel, name='sale_report_excel'),
    path('sale_report_pdf/', views.sale_report_pdf, name='sale_report_pdf'),
    path('sale_report_product_excel/', views.sale_report_product_excel, name='sale_report_product_excel'),
    path('sale_report_product_pdf/', views.sale_report_product_pdf, name='sale_report_product_pdf'),
    path('sale_report_excel_customer_wise/', views.sale_report_excel_customer_wise, name='sale_report_excel_customer_wise'),
    path('sale_report_pdf_customer_wise/', views.sale_report_pdf_customer_wise, name='sale_report_pdf_customer_wise'),
    path('finance_expense_report_excel/', views.finance_expense_report_excel, name='finance_expense_report_excel'),
    path('finance_expense_report_pdf/', views.finance_expense_report_pdf, name='finance_expense_report_pdf'),
    path('summery_report_pdf/', views.summery_report_pdf, name='summery_report_pdf'),
    path('summery_report_excel/', views.summery_report_excel, name='summery_report_excel'),
   
]