from django.shortcuts import render, HttpResponse
from .models import c
import time

def cron(request):
    if request.method == "GET":
        t = time.time()
        if c.objects.exists():
            obj = c.objects.first()
            obj.flag = t
            obj.save()
        else:
            new = c(flag=t)
            new.save()

        return HttpResponse(f"Woke up today at {t}")
    else:
        return HttpResponse("Invalid request")
