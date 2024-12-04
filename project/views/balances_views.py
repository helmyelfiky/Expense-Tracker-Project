from django.shortcuts import render
from project.models import UserBalance

def update_user_balance(transaction):
    user_balance = UserBalance.objects.get(user=transaction.user)

    if transaction.type == 'income':
        user_balance.income_balance += transaction.amount
    elif transaction.type == 'expense':
        user_balance.total_expenses += transaction.amount
    
    user_balance.update_balance()
