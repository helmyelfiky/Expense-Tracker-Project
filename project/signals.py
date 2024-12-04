from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserBalance, Category

@receiver(post_save, sender=CustomUser)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        print(f"Default categories created for user: {instance.username}")
        UserBalance.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_balance(sender, instance, **kwargs):
    if hasattr(instance, 'balance'):
        instance.balance.save()

@receiver(post_save, sender=CustomUser)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        # Default expense categories
        expense_categories = ['Food', 'Fuel', 'Shopping']
        # Default income categories
        income_categories = ['Salary', 'Loan']

        for category in expense_categories:
            if not Category.objects.filter(user=instance, Category_Name=category, Category_Type=Category.CategoryType.EXPENSE).exists():
                Category.objects.create(user=instance, Category_Name=category, Category_Type=Category.CategoryType.EXPENSE)

        for category in income_categories:
            if not Category.objects.filter(user=instance, Category_Name=category, Category_Type=Category.CategoryType.INCOME).exists():
                Category.objects.create(user=instance, Category_Name=category, Category_Type=Category.CategoryType.INCOME)