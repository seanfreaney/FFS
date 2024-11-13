from django import forms
from .models import ServiceRequest, Document

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = [
            'business_type', 
            'monthly_revenue', 
            'monthly_transactions', 
            'monthly_operating_costs'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monthly_operating_costs'].required = True
        self.fields['business_type'].required = True
        self.fields['monthly_revenue'].required = True
        self.fields['monthly_transactions'].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.status:
            instance.status = 'pending'  # Set default status
        if not instance.quote_status:
            instance.quote_status = 'pending'  # Set default quote status
        if commit:
            instance.save()
        return instance

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'is_bank_statement']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = True

    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        # Skip validation if no new file is uploaded
        if not file or not hasattr(file, 'content_type'):
            return file
            
        # Only validate new file uploads
        ext = file.name.split('.')[-1].lower()
        content_type = file.content_type
        
        # Define allowed types
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
        allowed_content_types = [
            'application/pdf',
            'image/jpeg',
            'image/png',
            'image/jpg'
        ]
        
        if ext not in allowed_extensions or content_type not in allowed_content_types:
            raise forms.ValidationError(
                'Invalid file type. Only PDF and image files (JPG, JPEG, PNG) are allowed.'
            )
        return file
