from django.urls import path
from .views import SendEmailView, home

urlpatterns = [
    path('send', SendEmailView.as_view(), name='email_client'),
    path('', home, name='home')
]