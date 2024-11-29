from django.shortcuts import render,HttpResponse

# Create your views here.
def user_home(request):
    return HttpResponse("hello user auth home")

def signup(request):
    return render(request, 'users_auth/signup.html')

def login(request):
    return render(request, 'users_auth/login.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomSignupForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import CustomUser

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user to the database
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('users_auth:login')  # Redirect to the login page
        else:
            messages.error(request, "There was an error creating your account. Please correct the errors below.")
    else:
        form = CustomSignupForm()
    
    return render(request, 'users_auth/signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Attempting to authenticate user: {username}")  # Debugging line

        # Use Django's built-in authentication system to check the password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"User authenticated: {user.username}")  # Debugging line
            login(request, user)

            # Redirect based on the user's admin status
            if user.is_admin:
                print("Redirecting to admin dashboard")  # Debugging line
                return redirect('tracker:admin_panel_dashboard')
            else:
                print("Redirecting to user dashboard")  # Debugging line
                return redirect('tracker:users_dashboard')

        else:
            print("Authentication failed!")  # Debugging line
            messages.error(request, 'Invalid username or password')  # Display error message
            return render(request, 'users_auth/login.html')

    # GET request, show the login form
    return render(request, 'users_auth/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('tracker:home')