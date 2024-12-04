from django import forms
from .import models

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['Transaction_type', 'Date', 'Category', 'Amount', 'Description']

        widgets ={
            'Date': forms.DateInput(
                attrs={
                    'type': 'date'
                }),
            'Amount': forms.NumberInput(
                attrs={
                    'min': '0'
                }
            ),
            'Description': forms.TextInput(),
            'Transaction_type': forms.RadioSelect(
                choices=[
                    ('Income', 'Income'),
                    ('Expense', 'Expense')
                ]
            )
        }
        
    Category = forms.ModelChoiceField(
        queryset=models.Category.objects.all(),
        empty_label="Select a category",  # Optional: default empty label
        widget=forms.Select(
            attrs={'class': 'form-control'})  # Custom styling
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['Category_Name', 'Category_Type']

        widgets = {
            'Category_Type': forms.RadioSelect(
                choices=[
                    ('Income', 'Income'),
                    ('Expense', 'Expense')
                ]
            ),
            'Category_Name': forms.TextInput()
        }
        
class TransactionsForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['Transaction_type', 'Date', 'Category', 'Amount', 'Description']
        widgets = {
            'Transaction_type': forms.RadioSelect(choices=[
                ('Income', 'Income'),
                ('Expense', 'Expense')
            ]),
            'Date': forms.DateInput(attrs={'type': 'date'}),
            'Category': forms.Select(),
            'Amount': forms.NumberInput(attrs={'min': '0'}),
            'Description': forms.TextInput()
        }

class EditTransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['Transaction_type', 'Date', 'Category', 'Amount', 'Description']
        widgets = {
            'Date': forms.DateInput(
                attrs={
                    'type': 'date'
                }),
            'Amount': forms.NumberInput(
                attrs={
                    'min': '0'
                }
            ),
            'Description': forms.TextInput(),
            'Transaction_type': forms.RadioSelect(
                choices=[
                    ('Income', 'Income'),
                    ('Expense', 'Expense')
                ]
            )
        }
    
class SignupForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'gender', 'account_type']
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
            'gender': forms.RadioSelect(
                choices=[
                    ('male', 'Male'),
                    ('female', 'Female')
                ]
            ),
            'account_type': forms.RadioSelect(
                choices=[
                    ('individual', 'Individual'),
                    ('family', 'Family')
                ]
            )   
        }
