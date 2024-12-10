from django.urls import path
from .views import login_view, logout_view, home_view, signup_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),  # Signup URL
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
]