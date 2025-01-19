from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Tax
from .froms import TaxForm

@login_required(login_url='signin')
def AddTax(request):
    if request.method == "POST":
        name = request.POST.get('name')
        tax_rate = request.POST.get('tax')
        tax = Tax.objects.create(tax_name = name,tax_percentage = tax_rate )
        tax.save()
        messages.success(request,'Tax Value Added Success')
        return redirect("ListTax")
    return render(request,"add-tax-slab.html")

@login_required(login_url='signin')
def ListTax(request):
    tax = Tax.objects.all()
    context = {
        "tax":tax
    }
    return render(request,"list-tax.html",context)

@login_required(login_url="signin")
def delete_tax(request,pk):
    tax = get_object_or_404(Tax,pk=pk)
    tax.delete()
    messages.success(request,'Tax Value Deleted Success')
    return redirect("ListTax")

@login_required(login_url="signin")
def tax_single_update(request,pk):
    tax = get_object_or_404(Tax,pk=pk)
    form = TaxForm(instance = tax)
    if request.method == "POST":
        form = TaxForm(request.POST,instance = tax)
        if form.is_valid():
            tax = form.save()
            tax.save()
            messages.success(request,'Tax Value Updated Success')
            return redirect("ListTax")
    return render(request,"tax-single.html",{"form":form})



    
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from .models import *
from service.models import Order
from .forms import *
from django.shortcuts import render
from django.utils.timezone import now
from .models import Income, Expense
from itertools import chain
from operator import attrgetter
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required 

@login_required(login_url="SignIn")
def income(request):
    income = Income.objects.all().order_by("-id")

    context = {
        "income":income
    }
    return render(request,"finance/income.html",context)


@login_required(login_url="SignIn")
def add_income(request):
    form = IncomeForm()

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Income record added successfully.")
            return redirect('income')  # Redirect to the same page or another view
 
    return render(request, 'finance/add-income.html', {'form': form})

@login_required(login_url="SignIn")
def update_income(request,pk):
    income  = get_object_or_404(Income,id = pk)
    form = IncomeForm(instance=income)

    if request.method == 'POST':
        form = IncomeForm(request.POST,instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, "Income Update successfully.")
            return redirect('income')  # Redirect to the same page or another view
 
    return render(request, 'finance/update-income.html', {'form': form})


@login_required(login_url="SignIn")
def delete_income(request,pk):
    income = get_object_or_404(Income,id = pk)
    income.delete()
    messages.success(request,"Income deleted success.....")
    return redirect("income")



@login_required(login_url="SignIn")
def expence(request):
    ex = Expense.objects.all().order_by("-id")
    context = {
        "expence":ex
    }
    return render(request,"finance/expence.html",context)


@login_required(login_url="SignIn")
def delete_expense(request,pk):
    expense = get_object_or_404(Expense,id = pk)
    expense.delete()
    messages.success(request,"Expense deleted success.....")
    return redirect("expence")


# View for adding expense
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense record added successfully.")
            return redirect('expence')  # Redirect to the same page or another view
    else:
        form = ExpenseForm()
    return render(request, 'finance/add-expense.html', {'form': form})

def update_expense(request,pk):
    expense = get_object_or_404(Expense, id = pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense record added successfully.")
            return redirect('expence')  # Redirect to the same page or another view
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'finance/update-expense.html', {'form': form})




def balance_sheet(request):
    # Get the current date
    current_date = now()
    month = current_date.strftime("%B")

    # Filter income and expenses for the current month
    income_list = Income.objects.filter(date__year=current_date.year, date__month=current_date.month)
    expense_list = Expense.objects.filter(date__year=current_date.year, date__month=current_date.month)

    # Convert to lists with 'type' field indicating credit (income) or debit (expense)
    income_data = [{'type': 'credit', 'date': income.date, 'particulars': income.particulars, 'amount': income.amount} for income in income_list]
    expense_data = [{'type': 'debit', 'date': expense.date, 'particulars': expense.particulars, 'amount': expense.amount} for expense in expense_list]

    # Combine both lists and order by date
    combined_list = sorted(
        chain(income_data, expense_data),
        key=lambda x: x['date']
    )

    # Calculate totals
    total_income = sum(income['amount'] for income in income_data)
    total_expense = sum(expense['amount'] for expense in expense_data)

    # Pass data to the template
    return render(request, "finance/balancesheet.html", {
        'combined_list': combined_list,
        'total_income': total_income,
        'total_expense': total_expense,
        "month":month
    })


from django.shortcuts import render
from django.utils.timezone import now
from .models import Income, Expense
from itertools import chain
from operator import attrgetter

def balance_sheet_selected(request):
    if request.method == "POST":
    # Get start and end dates from form submission (default to current month if not provided)
        start_date = request.POST.get('sdate')
        end_date = request.POST.get('edate')

    if start_date and end_date:
        # Filter by selected date range
        income_list = Income.objects.filter(date__range=[start_date, end_date])
        expense_list = Expense.objects.filter(date__range=[start_date, end_date])
    else:
        # Default to current month if no dates are provided
        current_date = now()
        income_list = Income.objects.filter(date__year=current_date.year, date__month=current_date.month)
        expense_list = Expense.objects.filter(date__year=current_date.year, date__month=current_date.month)

    # Convert to lists with 'type' field indicating credit (income) or debit (expense)
    income_data = [{'type': 'credit', 'date': income.date, 'particulars': income.particulars, 'amount': income.amount} for income in income_list]
    expense_data = [{'type': 'debit', 'date': expense.date, 'particulars': expense.particulars, 'amount': expense.amount} for expense in expense_list]

    # Combine both lists and order by date
    combined_list = sorted(
        chain(income_data, expense_data),
        key=lambda x: x['date']
    )

    # Calculate totals
    total_income = sum(income['amount'] for income in income_data)
    total_expense = sum(expense['amount'] for expense in expense_data)

    # Pass data to the template
    return render(request, "finance/balancesheet.html", {
        'combined_list': combined_list,
        'total_income': total_income,
        'total_expense': total_expense,
        'start_date': start_date,
        'end_date': end_date,
        "month": f"{start_date} to {end_date}"
    })


# bullk delete 


#Bulk Delete




def delete_bulk_invoice(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('contact_id[]')  # Get the selected IDs from the form
        print(selected_ids,"----------------------------------")
        if selected_ids:
            Order.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'Selected items have been deleted.')
        else:
            messages.warning(request, 'No items were selected for deletion.')
    return redirect("list_sale")


def delete_bulk_invoice_pending(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('contact_id[]')  # Get the selected IDs from the form
        print(selected_ids,"----------------------------------")
        if selected_ids:
            Order.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'Selected items have been deleted.')
        else:
            messages.warning(request, 'No items were selected for deletion.')
    return redirect("list_sale_pending")


def delete_bulk_invoice_partial(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('contact_id[]')  # Get the selected IDs from the form
        print(selected_ids,"----------------------------------")
        if selected_ids:
            Order.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'Selected items have been deleted.')
        else:
            messages.warning(request, 'No items were selected for deletion.')
    return redirect("list_sale_partial")


def delete_bulk_income(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('contact_id[]')  # Get the selected IDs from the form
        print(selected_ids,"----------------------------------")
        if selected_ids:
            Income.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'Selected items have been deleted.')
        else:
            messages.warning(request, 'No items were selected for deletion.')
    return redirect("income")

def delete_bulk_expense(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('contact_id[]')  # Get the selected IDs from the form
        print(selected_ids,"----------------------------------")
        if selected_ids:
            Expense.objects.filter(id__in=selected_ids).delete()
            messages.success(request, 'Selected items have been deleted.')
        else:
            messages.warning(request, 'No items were selected for deletion.')
    return redirect("expence")



@login_required(login_url='signin')
def tax_calculation(request):
    from datetime import datetime
    from django.db.models import Sum
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Filter orders for the current month and year
    orders = Order.objects.filter(order_date__year=current_year, order_date__month=current_month)

    # Calculate total tax for the current month
    total_tax = orders.aggregate(Sum('total_tax'))['total_tax__sum'] or 0

        # Check if the form is submitted
    if request.method == "POST":
        start_date = request.POST.get('sdate')
        end_date = request.POST.get('edate')

        if start_date and end_date:
            # Filter orders within the date range
            orders = orders.filter(order_date__date__gte=start_date, order_date__date__lte=end_date)
            total_tax = orders.aggregate(Sum('total_tax'))['total_tax__sum'] or 0

    # Prepare the data for the template
    combined_list = [
        {
            'date': order.order_date,
            'particulars': f"Order {order.invoice_number}",
            'tax_amount': order.total_tax,
        }
        for order in orders
    ]

    # Render the template with the data
    return render(request, "finance/tax.html", {
        'combined_list': combined_list,
        'total_tax': total_tax,
        'month': datetime.now().strftime('%B')  # Current month name
    })


#+================================================================================================================================================
#+================================================================================================================================================
#+================================================================================================================================================
#+================================================================================================================================================
#+================================================================================================================================================
# reports

from service.models import Customers, Services, OrderItem



def reports(request):
    customer = Customers.objects.all()
    product = Services.objects.all()
  
    

    context = {
        "customer":customer,
        "product":product,
      
    }
    return render(request,"reports.html",context)


from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
import pandas as pd
from openpyxl.styles import Border, Side
from django.db.models import Sum
import os
from django.conf import settings

def download_db(request):
    # Path to your SQLite database file
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    
    # Check if the file exists
    if os.path.exists(db_path):
        with open(db_path, 'rb') as db_file:
            response = HttpResponse(db_file.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = 'attachment; filename="db.sqlite3"'
            return response
    else:
        raise HttpResponse("Database not found.")

def expence_report_excel(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        payment_mode = request.POST.get("mode_payment")

        if payment_mode == "all":
        # Filter expenses based on the date range
            expenses = Expense.objects.filter(date__range=[start_date, end_date])
        else:
            expenses = Expense.objects.filter(date__range=[start_date, end_date],payment_mode = payment_mode)


        # Convert expenses to a Pandas DataFrame
        data = {
            'Date': [exp.date for exp in expenses],
            'Particulars': [exp.particulars for exp in expenses],
            'Amount': [exp.amount for exp in expenses],
            'Other': [exp.other for exp in expenses],
        }
        df = pd.DataFrame(data)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="expense_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')

        return response


def expence_report_pdf(request):
   
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        payment_mode = request.POST.get("mode_payment")

        if payment_mode == "all":
        # Filter expenses based on the date range
            expenses = Expense.objects.filter(date__range=[start_date, end_date])
        else:
            expenses = Expense.objects.filter(date__range=[start_date, end_date],payment_mode = payment_mode)
        # Calculate subtotal for amount

        subtotal = expenses.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    
        # Render the data to a template
        template_path = 'expense_report_pdf.html'
        context = {
            'expenses': expenses,
            'start_date': start_date,
            'end_date': end_date,
            "subtotal":subtotal,
            
        }
        html = render_to_string(template_path, context)

        # Create a PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="expense_report_{start_date}_to_{end_date}.pdf"'

        # Create PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )

        # If there's an error, show it in the response
        if pisa_status.err:
            return HttpResponse('We had some errors with the report')

        return response


def income_report_excel(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        payment_mode = request.POST.get("mode_payment")

        # Filter expenses based on the date range
        if payment_mode == "all":
            expenses = Income.objects.filter(date__range=[start_date, end_date])
        else:
            expenses = Income.objects.filter(date__range=[start_date, end_date],payment_mode = payment_mode )
        
        # Convert expenses to a Pandas DataFrame
        data = {
            'Date': [exp.date for exp in expenses],
            'Particulars': [exp.particulars for exp in expenses],
            'Amount': [exp.amount for exp in expenses],
            'Other': [exp.other for exp in expenses],
        }
        df = pd.DataFrame(data)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Income_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')

        return response


def income_report_pdf(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        payment_mode = request.POST.get("mode_payment")

        # Filter expenses based on the date range
        if payment_mode == "all":
            income = Income.objects.filter(date__range=[start_date, end_date])
        else:
            income = Income.objects.filter(date__range=[start_date, end_date],payment_mode = payment_mode )
        

        subtotal = income.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        # Render the data to a template
        template_path = 'income_report_pdf.html'
        context = {
            'income': income,
            'start_date': start_date,
            'end_date': end_date,
            "subtotal":subtotal
        }
        html = render_to_string(template_path, context)

        # Create a PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="income_report_{start_date}_to_{end_date}.pdf"'

        # Create PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )

        # If there's an error, show it in the response
        if pisa_status.err:
            return HttpResponse('We had some errors with the report')

        return response
    

# sale report 

def sale_report_excel(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        category = request.POST.get("category")

        # Filter orders based on the date range
        if not category:
            orders = Order.objects.filter(order_date__range=[start_date, end_date])
        else:
            orders = Order.objects.filter(order_date__range=[start_date, end_date], payment_status1=category)

        # Prepare data for the report
        data = {
            'Date': [order.order_date.replace(tzinfo=None) for order in orders],
            'Invoice Number': [order.invoice_number for order in orders],
            "Customer":[order.customer for order in orders],
            # Concatenate the product names from OrderItem for each order
            'Products': [', '.join([item.service.title for item in order.orderitem_set.all()]) for order in orders],
            'Amount': [order.total_amount for order in orders],
            'Paid Amount': [order.paid_amount for order in orders],
            'Balance Amount': [order.balance_amount for order in orders],
            'Payment Status': [order.payment_status1 for order in orders],
        }

        # Convert the data into a DataFrame
        df = pd.DataFrame(data)

        # Calculate totals
        totals = {
            'Date': 'Total',  # Label for the total row
            'Invoice Number': '',
            'Products': '',
            'Amount': df['Amount'].sum(),
            'Paid Amount': df['Paid Amount'].sum(),
            'Balance Amount': df['Balance Amount'].sum(),
            'Payment Status': '',
        }

        # Append total row to the DataFrame
        totals_df = pd.DataFrame([totals])
        df = pd.concat([df, totals_df], ignore_index=True)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="sale_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')
        

        return response

    
def sale_report_pdf(request):


    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        category = request.POST.get("category")

        # Filter orders based on the date range
        if not category:
            orders = Order.objects.filter(order_date__range=[start_date, end_date])
        else:
            orders = Order.objects.filter(order_date__range=[start_date, end_date], payment_status1=category)

        # Calculate totals
        total_amount = sum(order.total_amount for order in orders)
        total_paid = sum(order.payed_amount for order in orders)
        total_balance = sum(order.balance_amount for order in orders)

        # Prepare the context for the PDF template
        context = {
            'orders': orders,
            'start_date': start_date,
            'end_date': end_date,
            'total_amount': total_amount,
            'total_paid': total_paid,
            'total_balance': total_balance,
            
        }

        # Load the HTML template
        template = get_template('sale_report_pdf.html')
        html = template.render(context)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="sale_report_{start_date}_to_{end_date}.pdf"'

        # Create the PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse(f'We had some errors: {pisa_status.err}')
        return response
    


def sale_report_product_excel(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        product_id = request.POST.get("product")

        # Filter OrderItems based on the date range and optionally by product
        order_items = OrderItem.objects.filter(
            order__order_date__range=[start_date, end_date]
        )

        # If a product is specified, filter by product as well
        if product_id:
            order_items = order_items.filter(product_id=product_id)

        # Prepare data for the report
        data = {
            'Order Number': [order_item.order.invoice_number for order_item in order_items],
            'Date of Order': [order_item.order.order_date.replace(tzinfo=None) for order_item in order_items],
            'Product': [order_item.product.name for order_item in order_items],
            'Quantity': [order_item.quantity for order_item in order_items],
            'Unit Price': [order_item.unit_price for order_item in order_items],
            'Discount': [order_item.discount for order_item in order_items],
            'Total Price': [order_item.total_price for order_item in order_items],
            
        }

        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="sale_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')

        return response
    

import io

def sale_report_product_pdf(request):
    if request.method == "POST":
        # Get the start and end date from the form
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        product_id = request.POST.get("product")
        
        orders = Order.objects.filter(order_date__range=[start_date, end_date])
        if product_id:
            orders = orders.filter(orderitem__product_id=product_id)

        # Calculate totals
        total_amount = sum(order.total_amount for order in orders)
        total_paid = sum(order.paid_amount for order in orders)
        total_balance = sum(order.balance_amount for order in orders)

        # Render HTML content
        html_content = render_to_string("sales_report_template.html", {
            "orders": orders,
            "total_amount": total_amount,
            "total_paid": total_paid,
            "total_balance": total_balance,
            "start_date": start_date,
            "end_date": end_date,
              # Replace with the actual path to the logo image
        })

        # Create a PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="sale_report_{start_date}_to_{end_date}.pdf"'

        # Use xhtml2pdf to generate the PDF
        pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=response)

        # Check if there was an error
        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)
        
        return response

    
def sale_report_excel_customer_wise(request):
    if request.method == "POST":
        # Get the start and end date from the form, along with the selected customer
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        selected_customer = request.POST.get("customer")  # Customer filter
        payment_status = request.POST.get("payment_status")

        # Filter orders based on the date range and customer (if selected)
        if selected_customer:
            orders = Order.objects.filter(
                order_date__range=[start_date, end_date],
                customer_id=selected_customer
            )
        else:
            orders = Order.objects.filter(order_date__range=[start_date, end_date])

        if payment_status == "PAID":
            orders = orders.filter(payment_status1 = "PAID")
        elif payment_status == "UNPAID":
            orders = orders.filter(payment_status1 = "UNPAID")
        elif payment_status == "PARTIALLY":
            orders = orders.filter(payment_status1 = "PARTIALLY")
        elif payment_status == "pending":
            orders = orders.filter(Q(payment_status1="PARTIALLY") | Q(payment_status1="UNPAID") )

        # Prepare product-wise data
        data = {
            'Customer': [],
            'Product': [],
            'Total Price': [],
            'Order Date': [],
            'Invoice Number': [],
            'Paid Amount': [],
            'Discount': [],
            'Balance Amount': [],
            'Payment Status': [],
        }

        for order in orders:
            for item in order.orderitem_set.all():
                data['Customer'].append(order.customer.name if order.customer else 'Cash Customer')
                data['Product'].append(item.service.title)
                data['Total Price'].append(item.total_price)
                data['Order Date'].append(order.order_date.replace(tzinfo=None))
                data['Invoice Number'].append(order.invoice_number)
                data['Paid Amount'].append(order.paid_amount)
                data['Discount'].append(order.discount)
                data['Balance Amount'].append(order.balance_amount)
                data['Payment Status'].append(order.payment_status1)

        # Convert the data into a DataFrame
        df = pd.DataFrame(data)

        # Calculate totals
        total_row = {
            'Customer': 'Total',
            'Product': '',
            'Total Price': df['Total Price'].sum(),
            'Order Date': '',
            'Invoice Number': '',
            'Paid Amount': df['Paid Amount'].sum(),
            'Discount': df['Discount'].sum(),
            'Balance Amount': df['Balance Amount'].sum(),
            'Payment Status': '',
        }

        # Convert total_row to DataFrame and concatenate
        total_df = pd.DataFrame([total_row])
        df = pd.concat([df, total_df], ignore_index=True)

        # Create an HttpResponse object with Excel content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Customer_sale_report_{start_date}_to_{end_date}.xlsx"'

        # Write the DataFrame to an Excel file
        df.to_excel(response, index=False, engine='openpyxl')

        return response


from django.db.models import Q
def sale_report_pdf_customer_wise(request):
    from datetime import datetime
    
    if request.method == "POST":
        # Get the start and end date from the form, along with the selected customer
        start_date = request.POST['sdate']
        end_date = request.POST['edate']
        selected_customer = request.POST.get("customer")
        payment_status = request.POST.get("payment_status")

        # Filter orders based on the date range and customer
        if selected_customer:
            orders = Order.objects.filter(
                order_date__range=[start_date, end_date],
                customer_id=selected_customer
            )
            customer = Customers.objects.get(id = selected_customer)
        else:
            orders = Order.objects.filter(order_date__range=[start_date, end_date])
            customer = {"name":"All Customers"}

        if payment_status == "PAID":
            orders = orders.filter(payment_status1 = "PAID")
        elif payment_status == "UNPAID":
            orders = orders.filter(payment_status1 = "UNPAID")
        elif payment_status == "PARTIALLY":
            orders = orders.filter(payment_status1 = "PARTIALLY")
        elif payment_status == "pending":
            orders = orders.filter(Q(payment_status1="PARTIALLY") | Q(payment_status1="UNPAID") )


        # Prepare data and calculate totals
        data = []
        grand_total_sum = 0
        paid_amount_sum = 0
        open_amount_sum = 0

        for order in orders:
            due_date = order.order_date.date() if isinstance(order.order_date, datetime) else order.order_date
            days_due = (datetime.now().date() - due_date).days
            grand_total = order.total_amount_from_customer
            paid_amount = order.paid_amount
            open_amount = grand_total - paid_amount

            # Update total sums
            grand_total_sum += grand_total
            paid_amount_sum += paid_amount
            open_amount_sum += open_amount

            row = {
                'invoice_no': order.invoice_number,
                'order_no': 0,
                'date': order.order_date.strftime('%d-%b-%Y'),
                'payment_term_days': "Immediate",
                'due_date': due_date.strftime('%d-%b-%Y'),
                'grand_total': f"{grand_total:.2f}",
                'paid_amount': f"{paid_amount:.2f}",
                'open_amount': f"{open_amount:.2f}",
                'days_past_due': days_due if days_due > 0 else "N/A",
                
            }
            data.append(row)

        # Define the context for rendering the HTML template, including totals
        context = {
            'start_date': start_date,
            'end_date': end_date,
            'data': data,
            'totals': {
                'grand_total_sum': f"{grand_total_sum:.2f}",
                'paid_amount_sum': f"{paid_amount_sum:.2f}",
                'open_amount_sum': f"{open_amount_sum:.2f}"
            },
            "customer":customer,
            
        }

        # Render the HTML template to a string
        html = render_to_string('sale_report_template.html', context)

        # Generate the PDF from HTML
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{customer}_sale_report_{start_date}_to_{end_date}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Check for errors
        if pisa_status.err:
            return HttpResponse("An error occurred while generating the PDF", status=500)
        return response



from datetime import datetime, date
# summery report PDF 
def summery_report_pdf(request):
    if request.method == 'POST':
        
        # Get the start and end date from the request
        start_date = request.POST.get('sdate')
        end_date = request.POST.get('edate')

        # Convert to date format
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Filter records within the date range
        income_records = Income.objects.filter(date__range=[start_date, end_date])
        expense_records = Expense.objects.filter(date__range=[start_date, end_date])
        orders = Order.objects.filter(order_date__date__range=[start_date, end_date])
        

        # Calculate totals for income, expenses, and balances
        total_income = sum(record.amount for record in income_records)
        total_expense = sum(record.amount for record in expense_records)
        net_balance = total_income - total_expense

        # Calculate order totals and outstanding payments
        total_invoices_amount = sum(order.total_amount for order in orders)
        total_received = sum(order.paid_amount for order in orders)
        pending_amount = total_invoices_amount - total_received

        # Calculate purchase totals
        

        # Context for template
        context = {
            'income_records': income_records,
            'expense_records': expense_records,
            'orders': orders,
            
            'start_date': start_date,
            'end_date': end_date,
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'total_invoices_amount': total_invoices_amount,
            'total_received': total_received,
            'pending_amount': pending_amount,
           
            
        }

        # Render to PDF
        template = get_template('summery_report_date_pdf.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="summery_report_{start_date}_to_{end_date}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse(f'Error generating PDF: {pisa_status.err}')
        return response
    


def summery_report_excel(request):
    # Get start and end dates from the request
    if request.method == "POST":
        start_date = request.POST.get('sdate')
        end_date = request.POST.get('edate')
        
        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        
        # Fetch income and expense records within the date range
        income_records = Income.objects.filter(date__range=[start_date, end_date])
        expense_records = Expense.objects.filter(date__range=[start_date, end_date])
        
        # Prepare data for DataFrame
        income_data = {
            'Date': [record.date for record in income_records],
            'Particulars': [record.particulars for record in income_records],
            'Amount': [record.amount for record in income_records],
            'Account': ['Credit'] * len(income_records),
            'Bill Number': [record.bill_number for record in income_records],
            'Partner': [record.other for record in income_records],
        }
        expense_data = {
            'Date': [record.date for record in expense_records],
            'Particulars': [record.particulars for record in expense_records],
            'Amount': [record.amount for record in expense_records],
            'Account': ['Debit'] * len(expense_records),
            'Bill Number': [record.bill_number for record in expense_records],
            'Partner': [record.other for record in expense_records],
        }

        # Combine income and expense data into a single DataFrame
        combined_df = pd.concat([pd.DataFrame(income_data), pd.DataFrame(expense_data)], ignore_index=True)

        # Create summary DataFrame for totals
        total_income = combined_df[combined_df['Account'] == 'Credit']['Amount'].sum()
        total_expense = combined_df[combined_df['Account'] == 'Debit']['Amount'].sum()
        net_balance = total_income - total_expense
        summary_data = {
            'Category': ['Total Income', 'Total Expense', 'Net Balance'],
            'Amount': [total_income, total_expense, net_balance]
        }
        summary_df = pd.DataFrame(summary_data)

        # Prepare the HTTP response for an Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="finance_expense_report_{start_date}_to_{end_date}.xlsx"'

        # Write data to Excel
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            combined_df.to_excel(writer, sheet_name='Finance Report', index=False)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

        return response



def finance_expense_report_pdf(request):
    
    report_date = request.POST.get('report_date', date.today())

    # Fetch income, expenses, orders (invoices), and purchases for the specific day
    income_records = Income.objects.filter(date=report_date)
    expense_records = Expense.objects.filter(date=report_date)
    orders = Order.objects.filter(order_date__date=report_date)


    # Calculate totals for income, expenses, and balances
    total_income = sum(record.amount for record in income_records)
    total_expense = sum(record.amount for record in expense_records)
    net_balance = total_income - total_expense

    # Calculate order totals and outstanding payments
    total_invoices_amount = sum(order.total_amount for order in orders)
    total_received_today = sum(order.paid_amount for order in orders)
    pending_amount_today = total_invoices_amount - total_received_today

   

    # Context for template
    context = {
        'income_records': income_records,
        'expense_records': expense_records,
        'orders': orders,
        
        'report_date': report_date,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'total_invoices_amount': total_invoices_amount,
        'total_received_today': total_received_today,
        'pending_amount_today': pending_amount_today,
    }

    # Render to PDF
    template = get_template('finance_expense_report_pdf.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="finance_expense_report_{report_date}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f'Error generating PDF: {pisa_status.err}')
    return response


def finance_expense_report_excel(request):
    # Get date from the request, or default to today
    report_date = request.POST.get('report_date', date.today())

    # Fetch data
    income_records = Income.objects.filter(date=report_date)
    expense_records = Expense.objects.filter(date=report_date)

    # Prepare data for DataFrame
    income_data = {
        'Date': [record.date for record in income_records],
        'Particulars': [record.particulars for record in income_records],
        'Amount': [record.amount for record in income_records],
        'Account': ['Credit'] * len(income_records),
        'Bill Number': [record.bill_number for record in income_records],
        'Partner': [record.other for record in income_records],
    }
    expense_data = {
        'Date': [record.date for record in expense_records],
        'Particulars': [record.particulars for record in expense_records],
        'Amount': [record.amount for record in expense_records],
        'Account': ['Debit'] * len(expense_records),
        'Bill Number': [record.bill_number for record in expense_records],
        'Partner': [record.other for record in expense_records],
    }

    # Combine income and expense data
    combined_df = pd.concat([pd.DataFrame(income_data), pd.DataFrame(expense_data)], ignore_index=True)

    # Create summary DataFrame for totals
    summary_data = {
        'Category': ['Total Income', 'Total Expense', 'Net Balance'],
        'Amount': [combined_df[combined_df['Account'] == 'Credit']['Amount'].sum(),
                   combined_df[combined_df['Account'] == 'Debit']['Amount'].sum(),
                   combined_df[combined_df['Account'] == 'Credit']['Amount'].sum() -
                   combined_df[combined_df['Account'] == 'Debit']['Amount'].sum()]
    }
    summary_df = pd.DataFrame(summary_data)

    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="finance_expense_report_{report_date}.xlsx"'

    # Write DataFrames to Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        combined_df.to_excel(writer, sheet_name='Finance Report', index=False)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

    return response





