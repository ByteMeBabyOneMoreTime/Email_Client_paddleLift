from django.db import models
import uuid

class Client_Registration(models.Model):
    Company_name = models.CharField(max_length=2000)
    id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False  
    )

    def __str__(self):
        return str(self.Company_name) + " >> id: " +  str(self.id)

class Email_log(models.Model):
    SENT_STATUS_CHOICES = [
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    ]
    
    client = models.ForeignKey(Client_Registration, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=SENT_STATUS_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Email to {self.client.Company_name} - {self.status} at {self.sent_at}"