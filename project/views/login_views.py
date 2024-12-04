from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from project.models import CustomUser, Transaction, Category
from project.forms import ExpensesForm, SignupForm

# TO DISPLAY THE LOGIN PAGE
def index (request):
    return render(request, "project/login.html")

# # TO LOGIN INTO YOUR ACCOUNT
# def login_register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user and check_password(password, user.password):
#             login(request, user)
#             return redirect('project:dashboard')
#         else:
#             messages.error(request, 'Invalid username or password')
#     return render(request, 'project/login.html')

# # TO LOGIN INTO YOUR ACCOUNT
def login_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        print(f"Username: {username}, Password: {password}")  # Debugging line

        # Try to get the user by username
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None

        # Check if the user exists and verify the password
        if user and check_password(password, user.password):
            # Log the user in
            login(request, user)  

            # To Display Message When the user logs in 
            messages.success(request, f"Welcome, {user.first_name} {user.last_name}")
            print(f"welcome: {user.first_name} {user.last_name}")  # Debugging line
            
            # Redirect to expenses page
            return redirect('project:Dashboard')  
        else:
            messages.error(request, 'Invalid username or password.')  # Show error message
            return redirect('project:index')  # Redirect back to the login page
    return render(request, 'project/login.html')  # Render login page for GET request
