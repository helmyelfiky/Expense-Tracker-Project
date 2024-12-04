from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from project.models import Category, Transaction, UserBalance
from project.forms import CategoryForm, ExpensesForm, TransactionsForm, EditTransactionForm

# TO DISPLAY TRANSACTIONS PAGE
@login_required(login_url='project:login_register')
def transactions(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TransactionsForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('project:transactions')
    else:
        form = TransactionsForm()
    
    return render(request, 'project/transactions.html', {
        'form': form,
        'categories': categories
    })

# TO DISPLAY TRANSACTIONS LOGS
@login_required(login_url='project:login_register')
def transactions_all(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'project/transactions_logs.html', {
        'transactions': transactions
    })

# TO ADD TRANSACTION TO DATABASE
@login_required(login_url='project:login_register')
def add_transaction(request):
    categories = Category.objects.filter(user = request.user)
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction added successfully")
            user_balance = UserBalance.objects.get(user=transaction.user)

            if transaction.Transaction_type == 'Income':
                user_balance.income_balance += transaction.Amount
            elif transaction.Transaction_type == 'Expense':
                user_balance.total_expenses += transaction.Amount
                
            user_balance.update_balance()      

            return redirect('project:add_transaction')
        else:
            messages.error(request, "Failed to add transaction")
    else:
        form = ExpensesForm()
    return render(request, 'project/transactions.html', {
        'form': form,
        'categories': categories
    })

# TO EDIT TRANSACTION IN TRANSACTION LOGS
def edit_transaction(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('project:login_register'))

    transaction = get_object_or_404(Transaction, Transaction_ID=id)

    if request.method == 'POST':
        form = EditTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully")
            return redirect('project:transactions_all')
        else:
            messages.error(request, "Failed to update transaction")
    else:
        form = EditTransactionForm(instance=transaction)

    return render(request, 'project/edit_transaction.html', {
        'form': form,
        'transaction': transaction
    })

# TO DELETE TRANSACTION IN TRANSACTION LOGS
def delete_transaction(request, id):
    transaction = Transaction.objects.get(Transaction_ID=id)
    transaction.delete()
    messages.success(request, "Expenses Deleted Successfully")
    return redirect('project:transactions_all')