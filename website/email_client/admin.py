from django.contrib import admin

from .models import Client_Registration, Email_log
admin.site.register(Client_Registration)
admin.site.register(Email_log)