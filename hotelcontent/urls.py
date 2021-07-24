from .views import LoginView, RegistrationView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]