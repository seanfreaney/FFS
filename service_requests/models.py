from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class ServiceRequest(models.Model):
    request_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_type = models.CharField(max_length=100)
    monthly_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_transactions = models.IntegerField()
    monthly_operating_costs = models.DecimalField(max_digits=10, decimal_places=2)
    quote_amount = models.DecimalField(max_digits=10, decimal_places=2)
    quote_accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    is_bank_statement = models.BooleanField(default=True)
    is_completed_file = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Document for {self.service_request.request_number}"
