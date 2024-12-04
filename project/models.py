from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('family', 'Family'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    password = models.CharField(max_length=128, null=True)
    confirm_password = models.CharField(max_length=128, null=True)
    # user_balance = models.OneToOneField('UserBalance', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

class Family(models.Model):
    name = models.CharField(max_length=100)  # Family group name
    members = models.ManyToManyField(CustomUser, through='FamilyMembership', related_name='families')

    def get_family_balances(self):
        members = self.members.all()  # Assuming a related name for family membership
        income = sum(member.balance.income_balance for member in members if hasattr(member, 'balance'))
        expenses = sum(member.balance.total_expenses for member in members if hasattr(member, 'balance'))
        current = income - expenses
        return {'income': income, 'expenses': expenses, 'current': current}
    
    def __str__(self):
        return self.name

class FamilyMembership(models.Model):
    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('employee', 'Employee'),
        ('employer', 'Employer'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'family')  # Prevent duplicate memberships

    def __str__(self):
        return f"{self.user.username} in {self.family.name} as {self.role}"

class TransferTransaction(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_transfers')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def process_transfer(self):
        sender_balance = UserBalance.objects.get(user=self.sender)
        recipient_balance = UserBalance.objects.get(user=self.recipient)

        sender_balance.total_expenses += self.amount
        recipient_balance.income_balance += self.amount

        sender_balance.update_balance()
        recipient_balance.update_balance()

class Category(models.Model):
    class CategoryType(models.TextChoices):
        INCOME = 'Income', 'Income'
        EXPENSE = 'Expense', 'Expense'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='categories', default=1)
    Category_Name = models.CharField(max_length=64)
    Category_Type = models.CharField(
        max_length=7,
        choices=CategoryType.choices,
        default=CategoryType.EXPENSE,
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'Category_Name'], name='unique_category_per_user')
        ]

    def __str__(self):
        return self.Category_Name

User = get_user_model()

class Transaction(models.Model): 
    class Transaction_Type(models.TextChoices):
        INCOME = 'Income'
        EXPENSE = 'Expense'

    Date = models.DateField()
    Transaction_ID = models.BigAutoField(primary_key=True)
    Transaction_type = models.CharField(max_length=7, choices=Transaction_Type.choices, default=Transaction_Type.EXPENSE)
    Category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, blank=True, related_name="category")
    Amount = models.IntegerField()
    Description = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions", default=1)  # Replace 1 with the ID of the default user

    def __str__(self):
        return f"(Expense No.:{self.Transaction_ID} Transaction Type: {self.Transaction_type} Date:{self.Date} Category:{self.Category} Description: {self.Description} Amount = {self.Amount})"
    
class UserBalance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='balance')
    income_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_balance(self):
        self.current_balance = self.income_balance - self.total_expenses
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Balance"
    


