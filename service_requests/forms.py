from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['business_type', 'monthly_revenue', 'monthly_transactions', 'monthly_operating_costs']