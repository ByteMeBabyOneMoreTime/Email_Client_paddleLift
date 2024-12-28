from django.db import models

class c(models.Model):
    flag = models.IntegerField()
    def __str__(self) -> str:
        return f"{self.flag}"