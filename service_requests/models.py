from django.db import models
from django.contrib.auth.models import User
import uuid

# Define STATUS_CHOICES before the model
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

QUOTE_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]

class ServiceRequest(models.Model):
    request_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_type = models.CharField(max_length=100)
    monthly_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_transactions = models.IntegerField()
    monthly_operating_costs = models.DecimalField(max_digits=10, decimal_places=2)
    quote_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quote_accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quote_status = models.CharField(
        max_length=20, 
        choices=QUOTE_STATUS_CHOICES,
        default='pending'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('customer', 'Customer Document'),
        ('owner', 'Owner Document'),
    ]
    
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    is_bank_statement = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='customer')

    def __str__(self):
        return f"Document for {self.service_request.request_number}"

    def save(self, *args, **kwargs):
        if self.pk:
            # If this is an update, delete the old file
            old_document = Document.objects.get(pk=self.pk)
            if old_document.file != self.file:
                old_document.file.delete(save=False)
        super().save(*args, **kwargs)
