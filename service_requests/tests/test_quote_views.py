from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from service_requests.models import ServiceRequest
from decimal import Decimal

class QuoteResponseViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.service_request = ServiceRequest.objects.create(
            user=self.user,
            request_number='TEST001',
            status='pending',
            quote_status='pending',
            quote_amount=Decimal('100.00')
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_quote_response_accept(self):
        response = self.client.post(
            reverse('quote_response', 
                   kwargs={'request_number': self.service_request.request_number}),
            {'response': 'accepted'}
        )
        
        # Refresh from database
        self.service_request.refresh_from_db()
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(self.service_request.quote_status, 'accepted')
        self.assertEqual(self.service_request.status, 'in_progress')

    def test_quote_response_reject(self):
        response = self.client.post(
            reverse('quote_response', 
                   kwargs={'request_number': self.service_request.request_number}),
            {'response': 'rejected'}
        )
        
        # Refresh from database
        self.service_request.refresh_from_db()
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(self.service_request.quote_status, 'rejected')