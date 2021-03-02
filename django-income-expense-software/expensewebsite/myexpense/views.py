import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from . import models
from userprefrences.models import UserPreference
import datetime


# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    expenses = models.Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    data = {'expenses': expenses,
            'page_obj': page_obj,
            'currency': currency}
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


@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    expense = models.Expense.objects.get(pk=id)
    categories = models.Category.objects.all()
    context = {
        'expense': expense,
        'categories': categories,
        'values': expense
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = models.Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')


@login_required(login_url='/authentication/login')
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = models.Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | models.Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | models.Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | models.Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = models.Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')