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

    def test_edit_service_request(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'business_type': 'Updated Business',
            'monthly_revenue': '2000.00',
            'monthly_transactions': '200',
            'monthly_operating_costs': '1000.00',
            'file': SimpleUploadedFile("new_doc.pdf", b"new_content", content_type="application/pdf"),
            'is_bank_statement': True,
        }
        response = self.client.post(
            reverse('edit_service_request', kwargs={'request_number': self.service_request.request_number}),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.business_type, 'Updated Business')

    def test_quote_response(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('quote_response', kwargs={'request_number': self.service_request.request_number}),
            {'response': 'accepted'}
        )
        self.assertEqual(response.status_code, 302)
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.quote_status, 'accepted')

    def test_delete_service_request(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('delete_service_request', kwargs={'request_number': self.service_request.request_number})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ServiceRequest.objects.filter(request_number=self.service_request.request_number).exists())

    # Negative test cases
    def test_edit_service_request_unauthorized(self):
        # Create another user and login
        User.objects.create_user(username='otheruser', password='testpass123')
        self.client.login(username='otheruser', password='testpass123')
        
        response = self.client.get(
            reverse('edit_service_request', kwargs={'request_number': self.service_request.request_number})
        )
        self.assertEqual(response.status_code, 404)

    def test_quote_response_invalid_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('quote_response', kwargs={'request_number': self.service_request.request_number}),
            {'response': 'invalid_status'}
        )
        self.assertEqual(response.status_code, 302)
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.quote_status, 'pending')  # Status should remain unchanged

    def test_delete_service_request_unauthorized(self):
        # Create another user and login
        User.objects.create_user(username='otheruser', password='testpass123')
        self.client.login(username='otheruser', password='testpass123')
        
        response = self.client.post(
            reverse('delete_service_request', kwargs={'request_number': self.service_request.request_number})
        )
        self.assertEqual(response.status_code, 302)  # Should redirect with error message
        self.assertTrue(ServiceRequest.objects.filter(request_number=self.service_request.request_number).exists())

    # Test accessing protected views without login
    def test_views_require_login(self):
        # Define URL patterns and their required kwargs
        url_patterns = [
            ('create_service_request', {}),  # Create doesn't need request_number
            ('service_request_list', {}),
            ('service_request_detail', {'request_number': self.service_request.request_number}),
            ('edit_service_request', {'request_number': self.service_request.request_number}),
            ('quote_response', {'request_number': self.service_request.request_number}),
        ]
        
        for url_name, kwargs in url_patterns:
            response = self.client.get(reverse(url_name, kwargs=kwargs))
            self.assertEqual(response.status_code, 302)  # Should redirect to login
            self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_edit_nonexistent_service_request(self):
        self.client.login(username='testuser', password='testpass123')
        fake_uuid = uuid.uuid4()
        response = self.client.get(
            reverse('edit_service_request', kwargs={'request_number': fake_uuid})
        )
        self.assertEqual(response.status_code, 404)

    def test_quote_response_already_processed(self):
        self.client.login(username='testuser', password='testpass123')
        # First set the quote status to accepted
        self.service_request.quote_status = 'accepted'
        self.service_request.save()
        
        # Try to change it again
        response = self.client.post(
            reverse('quote_response', kwargs={'request_number': self.service_request.request_number}),
            {'response': 'rejected'}
        )
        self.assertEqual(response.status_code, 302)
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.quote_status, 'accepted')  

    def test_create_service_request_invalid_data(self):
        """Test service request creation with invalid form data"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'business_type': '',  # Required field left empty
        'monthly_revenue': 'invalid',  # Invalid decimal
        'monthly_transactions': -1,  # Invalid negative number
        'monthly_operating_costs': '500.00',
        'file': SimpleUploadedFile("test.txt", b"wrong_type"),  # Wrong file type
        'is_bank_statement': True,
        }
        response = self.client.post(reverse('create_service_request'), data)
        self.assertEqual(response.status_code, 200)  # Returns to form
        self.assertTrue(response.context['form'].errors)  # Should have form errors

    def test_edit_service_request_invalid_data(self):
        """Test service request edit with invalid form data"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'business_type': '',  # Required field left empty
            'monthly_revenue': 'invalid',
            'monthly_transactions': -1,
            'monthly_operating_costs': '500.00',
            'file': SimpleUploadedFile("test.txt", b"wrong_type"),
            'is_bank_statement': True,
        }
        response = self.client.post(
            reverse('edit_service_request', kwargs={'request_number': self.service_request.request_number}),
            data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_service_request_list_empty(self):
        """Test service request list view with no requests"""
        # Create new user with no requests
        new_user = User.objects.create_user(username='newuser', password='testpass123')
        self.client.force_login(new_user)
        
        response = self.client.get(reverse('service_request_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['service_requests']), 0)