from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_type = models.CharField(max_length=100)
    monthly_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_transactions = models.IntegerField()
    monthly_operating_costs = models.DecimalField(max_digits=10, decimal_places=2)
    quote_amount = models.DecimalField(max_digits=10, decimal_places=2)
    quote_accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

class Document(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    is_bank_statement = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
