from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from service_requests.models import ServiceRequest, Document
from decimal import Decimal
import uuid
from django.contrib.auth.models import User

class ServiceRequestViewTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test service request with ALL required fields
        self.service_request = ServiceRequest.objects.create(
            user=self.user,
            business_type='Test Business',
            monthly_revenue=Decimal('1000.00'),
            monthly_transactions=100,
            monthly_operating_costs=Decimal('500.00'),
            status='pending',
            quote_status='pending'
        )
        
        # Create test document
        self.test_file = SimpleUploadedFile(
            "test_doc.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        self.document = Document.objects.create(
            service_request=self.service_request,
            uploaded_by=self.user,
            file=self.test_file
        )
        self.client = Client()

    def test_create_service_request_get(self):
        # Login required for this view
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_service_request'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service_requests/create_service_request.html')

    def test_create_service_request_post(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Create a test file for the document form
        test_file = SimpleUploadedFile(
            "test_doc.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        data = {
            'business_type': 'Test Business',
            'monthly_revenue': '1000.00',
            'monthly_transactions': '100',
            'monthly_operating_costs': '500.00',
            'file': test_file,
            'is_bank_statement': True,
        }
        
        response = self.client.post(reverse('create_service_request'), data)
        
        # Debug output
        print("Response status:", response.status_code)
        if response.status_code != 302:
            print("Form errors:", response.context['form'].errors if 'form' in response.context else "No form in context")
            
        self.assertEqual(response.status_code, 302)  # Expect redirect on success
        self.assertTrue(ServiceRequest.objects.filter(business_type='Test Business').exists())

    def test_service_request_detail(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('service_request_detail', 
                   kwargs={'request_number': self.service_request.request_number})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service_requests/service_request_detail.html')

    def test_service_request_list(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('service_request_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service_requests/service_request_list.html')
        self.assertIn(self.service_request, response.context['service_requests'])