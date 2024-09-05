
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import StoreUserCreateView

app_name ="my_auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("register/", StoreUserCreateView.as_view(), name='register'),
    ]