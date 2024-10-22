from django import forms
from .models import ServiceRequest, Document

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['business_type', 'monthly_revenue', 'monthly_transactions', 'monthly_operating_costs']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'is_bank_statement']
