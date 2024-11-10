from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from service_requests.forms import ServiceRequestForm, DocumentForm

class ServiceRequestFormsTests(TestCase):
    def test_service_request_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'business_type': 'Test Business',
            'monthly_revenue': '1000.00',
            'monthly_transactions': '100',
            'monthly_operating_costs': '500.00',
        }
        form = ServiceRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_service_request_form_invalid_data(self):
        """Test form with missing required fields"""
        form_data = {
            'business_type': '',  # Required field
            'monthly_revenue': 'invalid',  # Invalid decimal
            'monthly_transactions': '',  # Changed from -1 to empty string to test required field
        }
        form = ServiceRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('business_type', form.errors)
        self.assertIn('monthly_revenue', form.errors)
        self.assertIn('monthly_transactions', form.errors)
        self.assertIn('monthly_operating_costs', form.errors)

    def test_document_form_valid_data(self):
        """Test document form with valid file"""
        file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        form_data = {'is_bank_statement': True}
        file_data = {'file': file}
        form = DocumentForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_document_form_invalid_file_type(self):
        """Test document form with invalid file type"""
        file = SimpleUploadedFile(
            "test.exe",
            b"file_content",
            content_type="application/x-msdownload"
        )
        form_data = {'is_bank_statement': True}
        file_data = {'file': file}
        form = DocumentForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)