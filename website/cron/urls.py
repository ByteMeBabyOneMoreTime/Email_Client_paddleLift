from django.urls import path
from . import views

urlpatterns = [
    path('', views.cron, name='cron')
]
