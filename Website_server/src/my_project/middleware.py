# my_project/middleware.py

from django.shortcuts import redirect
from django.contrib import messages

class CustomLoginRedirectMiddleware:
    """
    Middleware to add a message when the user is redirected to the login page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        validwithoutlogin = ['/accounts/login/', '/accounts/logout/', '/accounts/signup/']
        if not request.user.is_authenticated and request.path not in validwithoutlogin:
            # User tries to gain access without having first logged in
            messages.error(request, "Ho ho ho, not so fast there. Login first my young padawan...")
            return redirect('accounts:login')  # Redirect to the login page
        return self.get_response(request)
