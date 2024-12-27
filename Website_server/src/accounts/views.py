from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from accounts.models import UserProfile # custom user
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        # Check if the user is approved
        if not request.user.userprofile.is_approved:
            logout(request)
            messages.error(request, "Your account is pending approval. Please contact the admin.")
            return redirect('accounts:login')
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            # Check if the user is approved
            if user.userprofile.is_approved:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Your account is pending approval.")
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Validate the form data
        if password != password_confirm:
            messages.error(request, "Passwords do not match.") # render these errors in the signup.html
            return render(request, 'accounts/signup.html')

        # Check if the username is already taken by a user, either approved or unapproved
        existing_user = User.objects.filter(username=username).first()

        if existing_user:
            # Check if the existing user is unapproved
            user_profile = UserProfile.objects.filter(user=existing_user).first()

            if user_profile and not user_profile.is_approved:
                messages.error(request, "You already have an account awaiting approval with this username.")
                return render(request, 'accounts/signup.html')

            messages.error(request, "Username already exists.")
            return render(request, 'accounts/signup.html')

        user = User.objects.create_user(username=username, password=password)

        # Create profile and make it a pending account
        user_profile = UserProfile.objects.create(user=user, is_approved=False, role='viewer', access_level=3)

        login(request, user)
        messages.success(request, "Your account has been created, but is awaiting approval.")
        return redirect('accounts:login')
    return render(request, 'accounts/signup.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def home_view(request):
    if not request.user.userprofile.is_approved:
        messages.error(request, "Your account is pending approval. Please contact the admin.")
        return redirect('accounts:login')
    
    return render(request, 'my_project/home.html')
