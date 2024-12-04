from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

# TO LOGOUT OF ACCOUNT    
def logout_view(request):
    logout(request) #logs out the user
    messages.success(request, "You have been logged out successfully")
    return render(request, "project/login.html")