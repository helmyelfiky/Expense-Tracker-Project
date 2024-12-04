from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

from project.models import CustomUser

# TO VIEW PROFILE
@login_required(login_url='project:login_register')
def profile(request):
    if request.user.is_authenticated:
        print(f"User: {request.user.username}, First Name: {request.user.first_name}, Last Name: {request.user.last_name}")
    else:
        print("User is not authenticated.")
    user = CustomUser.objects.get(username=request.user)
    return render(request, "project/profile.html", {
        'user': user
    })

# TO EDIT PROFILE
@login_required(login_url='project:login_register')
def edit_profile(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(username=request.user)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        return redirect('project:profile')
    else:
        user = CustomUser.objects.get(username=request.user)
        return render(request, 'project/profile.html', {
            'user': user
        })
    
# TO DELETE PROFILE
@login_required(login_url='project:login_register')
def delete_profile(request):
    user = CustomUser.objects.get(username=request.user)
    user.delete()
    # MESSAGE
    print("Profile deleted successfully")
    messages.success(request, "Profile Deleted Successfully")
    return redirect('project:login_register')
