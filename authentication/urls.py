from django.urls import path
from .views import registrationView,usernameValidationView,EmailValidation,loginView,LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("register",csrf_exempt(registrationView.as_view()),name="register"),
    path("username_validation",csrf_exempt(usernameValidationView.as_view()), name="username_validation"),
    path("email_validation",csrf_exempt(EmailValidation.as_view()), name="email_validation"),
    path("login",csrf_exempt(loginView.as_view()), name="login"),
    path("logout",csrf_exempt(LogoutView.as_view()), name="logout"),
    
    ]