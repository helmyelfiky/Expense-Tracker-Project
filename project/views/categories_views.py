from django.contrib import messages
from django.shortcuts import render, redirect

from project import forms
from project.forms import CategoryForm
from project.models import Category

# TO DISPLAY CATEGORIES PAGE
def categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'project/categories.html', {
        'categories': categories
    })

# TO ADD CATEGORY TO DATABASE
def add_category(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['Category_Name']
            category_type = form.cleaned_data['Category_Type']
            # Check if the category already exists for the user
            if Category.objects.filter(user=request.user, Category_Name=category_name, Category_Type=category_type).exists():
                messages.error(request, "Category already exists")
            else:
                form.save(commit=False)
                form.instance.user = request.user
                form.save()
                messages.success(request, "Category Added Successfully")
                return redirect('project:categories')
        else:
            messages.error(request, "Failed to add category")
    else:
        form = CategoryForm()
    
    return render(request, 'project/categories.html', {
        'form': form,
        'categories': categories
    })

# TO DELETE CATEGORY FROM DATABASE
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, "Category Deleted Successfully")
    return redirect('project:categories')

# TO EDIT CATEGORY IN CATEGORIES PAGE
def edit_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully")
            return redirect('project:categories')
        else:
            messages.error(request, "Failed to update category")
    else:
        form = CategoryForm(instance=category)
    return render(request, 'project/categories.html', {
        'form': form
    })