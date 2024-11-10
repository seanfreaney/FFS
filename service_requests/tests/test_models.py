from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from service_requests.models import ServiceRequest, Document
from decimal import Decimal
from django.core.files.storage import default_storage
import os

class ServiceRequestModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.service_request = ServiceRequest.objects.create(
            user=self.user,
            business_type='Test Business',
            monthly_revenue=Decimal('1000.00'),
            monthly_transactions=100,
            monthly_operating_costs=Decimal('500.00'),
            status='pending',
            quote_status='pending'
        )

    def test_mark_as_paid(self):
        """Test mark_as_paid method updates status correctly"""
        self.service_request.mark_as_paid()
        self.assertTrue(self.service_request.is_paid)
        self.assertEqual(self.service_request.status, 'in_progress')

class DocumentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.service_request = ServiceRequest.objects.create(
            user=self.user,
            business_type='Test Business',
            monthly_revenue=Decimal('1000.00'),
            monthly_transactions=100,
            monthly_operating_costs=Decimal('500.00'),
            status='pending'
        )

    def test_document_str_representation(self):
        """Test the string representation of Document"""
        document = Document.objects.create(
            service_request=self.service_request,
            file=SimpleUploadedFile("test.pdf", b"file_content"),
            uploaded_by=self.user
        )
        expected_str = f"Document for {self.service_request.request_number}"
        self.assertEqual(str(document), expected_str)

    def test_document_file_update(self):
        """Test that old file is deleted when updating document"""
        # Create initial document
        initial_file = SimpleUploadedFile("test1.pdf", b"file_content1", content_type="application/pdf")
        document = Document.objects.create(
            service_request=self.service_request,
            file=initial_file,
            uploaded_by=self.user
        )
        
        # Store the initial file path
        initial_file_path = document.file.path
        
        # Update with new file
        new_file = SimpleUploadedFile("test2.pdf", b"file_content2", content_type="application/pdf")
        document.file = new_file
        document.save()
        
        # Check that new file exists in name (using in instead of endswith)
        self.assertIn('test2', document.file.name)
        
        # Check that old file no longer exists
        self.assertFalse(os.path.exists(initial_file_path))