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

from service.models import Customers, Services



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

        # Filter expenses based on the date range
        expenses = Expense.objects.filter(date__range=[start_date, end_date])

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
        # Filter expenses based on the date range
        expenses = Expense.objects.filter(date__range=[start_date, end_date])
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

        # Filter expenses based on the date range
        expenses = Income.objects.filter(date__range=[start_date, end_date])
        
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

        # Filter expenses based on the date range
        income = Income.objects.filter(date__range=[start_date, end_date])

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
    



