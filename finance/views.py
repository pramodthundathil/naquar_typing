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



    
