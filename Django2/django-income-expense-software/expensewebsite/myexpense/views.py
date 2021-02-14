from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from django.contrib import messages


# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    expenses = models.Expense.objects.filter(owner=request.user)
    data = {'expenses': expenses}
    return render(request, 'expenses/index.html', data)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = models.Category.objects.all()
    data = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', data)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        expense_date = request.POST['expense_date']
        if not amount:
            messages.error(request, 'Amount should be provided')
        if not description:
            messages.error(request, 'Description is required')
        if not category:
            messages.error(request, 'Category is required')
        if not expense_date:
            messages.error(request, 'Date is required')

        else:
            models.Expense.objects.create(owner=request.user, amount=amount, date=expense_date,
                                          category=category, description=description)
            messages.success(request, 'Expense saved successfully')
            return redirect('expenses')
        return render(request, 'expenses/add_expense.html', data)
