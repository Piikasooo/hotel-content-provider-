from .views import LoginView, RegistrationView, HomePageView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('homepage/<username>/', HomePageView.as_view(), name='homepage'),
]