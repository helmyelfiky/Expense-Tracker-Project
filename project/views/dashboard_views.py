from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
import json
from django.utils.timezone import now
from django.db.models import Sum
from django.utils import timezone

from project.models import Transaction, Category, UserBalance

# TO VIEW DASHBOARD
# def dashboard(request):
#     expenses = Transaction.objects.all()
#     categories = Category.objects.all()
#     print(categories)  # Debugging line to check if categories are being fetched
#     return render(request, "project/dashboard.html", {
#         'expenses': expenses,
#         'categories': categories
#     })

# def dashboard(request):
#     expenses = Transaction.objects.all()
#     categories = Category.objects.all()
#     if request.user.is_authenticated:
#         balance = request.user.balance
#         context = {
#             'income': balance.income_balance,
#             'expenses': balance.total_expenses,
#             'current': balance.current_balance,
#             'expenses': expenses,
#             'categories': categories
#         }

#         if request.user.account_type == 'family' and 'view_family' in request.GET:
#             family_balances = request.user.family.get_family_balances()
#             context.update(family_balances)

#         return render(request, 'project/dashboard.html', context)
#     return redirect('project:login_register')


# TO VIEW DASHBOARD
@login_required(login_url='project:login_register')
def dashboard(request):
    if request.user.is_authenticated:
        # Ensure the user has a balance record
        if not hasattr(request.user, 'balance'):
            UserBalance.objects.create(user=request.user)
        
        balance = request.user.balance
        expenses = Transaction.objects.filter(user=request.user)
        categories = Category.objects.filter(user=request.user)
        Total_Amount = Transaction.objects.filter(user=request.user).aggregate(Sum('Amount'))['Amount__sum']
        
        # Get the current month and year
        current_month = timezone.now().month
        current_year = timezone.now().year

        # Filter transactions for the current month
        monthly_expenses = Transaction.objects.filter(
            user=request.user,
            Date__year=current_year,
            Date__month=current_month
        )

        # Calculate the total amount spent per category for the current month
        monthly_category_totals = (
            monthly_expenses
            .values('Category__Category_Name')
            .annotate(total_amount=Sum('Amount'))
        )
        monthly_category_totals_dict = {item['Category__Category_Name']: item['total_amount'] for item in monthly_category_totals}

        # Prepare data for the pie chart and total amount per category
        piechart_data = (
            Transaction.objects.filter(user=request.user)
            .values('Category__Category_Name')
            .annotate(total_amount=Sum('Amount'))
        )
        chart_labels = [item['Category__Category_Name'] for item in piechart_data]
        chart_data = [item['total_amount'] for item in piechart_data]

        # Prepare total amount per category
        category_totals = {item['Category__Category_Name']: item['total_amount'] for item in piechart_data}

        # Debugging
        print("Chart labels", chart_labels)
        print("Chart data", chart_data)
        print("Category totals", category_totals)
        print("Monthly category totals", monthly_category_totals_dict)

        context = {
            'income': balance.income_balance,
            'total_expenses': balance.total_expenses,
            'current': balance.current_balance,
            'expenses': expenses,
            'categories': categories,
            'Total_Amount': Total_Amount,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data),
            'category_totals': category_totals,
            'monthly_category_totals': monthly_category_totals_dict,
        }

        # Handle family balance logic if applicable
        if request.user.account_type == 'family' and 'view_family' in request.GET:
            family_balances = request.user.family.get_family_balances()
            context.update(family_balances)

        return render(request, 'project/dashboard.html', context)
    return redirect('project:login_register')

@login_required(login_url='project:login_register')
def piechart(request):
    user = request.user
    data = (
        Transaction.objects.filter(user=user)
        .values('Category__Category_Name')
        .annotate(total_amount=models.Sum('Amount'))
    )

    # prepare data for chart
    chart_data = {
        'labels': [item['Category__Category_Name'] for item in data],
        'data': [item['total_amount'] for item in data],
    }
    return JsonResponse(chart_data)
