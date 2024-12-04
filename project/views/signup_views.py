from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages


from project.models import CustomUser, Transaction, Category, Family, FamilyMembership
from project.forms import ExpensesForm, SignupForm

# TO DISPLAY THE SIGNUP PAGE
def register_user(request):
    return render(request, "project/register.html")

# TO CREATE AN ACCOUNT
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Do not save the user yet
            user.password = make_password(form.cleaned_data['password'])  # Hash the password
            user.confirm_password = make_password(form.cleaned_data['confirm_password'])  # Hash the password
            user.save()  # Save the user with the hashed password

            # If the user is creating a family account, create a family group
            if user.account_type == 'family':
                family = Family.objects.create(name=f"{user.username}'s Family")
                FamilyMembership.objects.create(user=user, family=family, role='parent')
            return redirect('project:login_register')  # Redirect to the login page
    else:
        form = SignupForm()
    return render(request, 'project/signup.html', {'form': form})


# # TO SIGN UP
# def signup(request):
#     if request.method == 'POST':
#         first_name = request.POST['First_name']
#         last_name = request.POST['Last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         password = make_password(request.POST['password'])  # Hash the password
#         gender = request.POST['gender']

#         # Create a new User object and save it to the database
#         try:
#             user = CustomUser(
#                 first_name=first_name,
#                 last_name=last_name,
#                 username=username,
#                 email=email,
#                 password=password,
#                 gender=gender
#             )
#             user.save()
#             messages.success(request, 'Your account has been created successfully!')
#             return redirect('project:index')  # To go back to login page after creating an account
#         except Exception as e:
#             print(f"Error: {e}")
#             messages.error(request, 'There was an issue creating your account.')

#         return redirect('project:signup')  # Redirect to the login page after registration
#     return render(request, 'project/register.html')  # Render the registration form if not a POST request
