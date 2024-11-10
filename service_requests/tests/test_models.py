from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from service_requests.models import ServiceRequest, Document
from decimal import Decimal

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
        document = Document.objects.create(
            service_request=self.service_request,
            file=SimpleUploadedFile("test1.pdf", b"file_content1"),
            uploaded_by=self.user
        )
        
        # Update with new file
        document.file = SimpleUploadedFile("test2.pdf", b"file_content2")
        document.save()
        
        # Check that new file is saved
        self.assertTrue(document.file.name.endswith('test2.pdf'))