from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from project.views.login_views import login_register, index
from project.views.signup_views import register_user, signup
from project.views.categories_views import categories, add_category, delete_category, edit_category
from project.views.transactions_views import transactions, add_transaction, transactions_all, edit_transaction, delete_transaction
from project.views.dashboard_views import dashboard, piechart
from project.views.profile_views import profile, edit_profile, delete_profile
from project.views.logout_views import logout_view
from project.views.balances_views import update_user_balance
from project.views.family_views import family

app_name = "project"
urlpatterns = [

    path("", index, name="index"),

    # SIGNUP
    path("Register", register_user, name="register"),
    path("signup", signup, name="signup"),

    # LOGIN AND LOGOUT
    path("logout", logout_view, name="logout_view"),
    path("login_register", login_register, name="login_register"),
    
    # CATEGORIES
    path("Categories", categories, name="categories"),    
    path("Add-Category", add_category, name="add_category"),
    path('delete-category/<int:id>/', delete_category, name='delete_category'),
    path('edit-category/<int:id>/', edit_category, name='edit_category'),

    # TRANSACTIONS
    path("Transactions", transactions, name="transactions"),
    path("Add-Transaction", add_transaction, name="add_transaction"),
    path("Transaction-Logs", transactions_all, name="transactions_all"),
    path("Edit-Transaction", edit_transaction, name="edit_transaction"),
    path("Delete-Transaction", delete_transaction, name="delete_transaction"),
    path('edit-transaction/<int:id>/', edit_transaction, name='edit_transaction'),
    path('delete-transaction/<int:id>/', delete_transaction, name='delete_transaction'),
    
    # DASHBOARD
    path("dashboard", dashboard, name="Dashboard"),
    path("piechart", piechart, name="Piechart"),

    # PROFILE
    path("Profile", profile, name="Profile"),
    path("Edit-Profile", edit_profile, name="edit_profile"),
    path("Delete-Profile", delete_profile, name="delete_profile"),

    
    # BALANCES
    path("update_balance", update_user_balance, name="update_balance"),

    # FAMILY
    path("family", family, name="family"),
    
]
