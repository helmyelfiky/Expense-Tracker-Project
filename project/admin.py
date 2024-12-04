from django.contrib import admin
from .models import Category, Transaction, CustomUser, Family, FamilyMembership

# Register your models here.
admin.site.register(Family)
admin.site.register(FamilyMembership)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Transaction)