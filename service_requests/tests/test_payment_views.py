from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from service_requests.models import ServiceRequest
from decimal import Decimal
import stripe
from unittest.mock import patch

class PaymentViewTests(TestCase):
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
            quote_status='accepted',
            quote_amount=Decimal('100.00'),
            is_paid=False
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    @patch('stripe.PaymentIntent.create')
    def test_create_payment_intent(self, mock_create):
        # Mock the Stripe API response
        mock_create.return_value = type('obj', (object,), {
            'client_secret': 'test_secret',
            'id': 'test_id'
        })

        response = self.client.post(
            reverse('create_payment_intent', 
                   kwargs={'request_number': self.service_request.request_number})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'clientSecret': 'test_secret',
                'requestNumber': self.service_request.request_number
            }
        )

    def test_check_payment_status(self):
        response = self.client.get(
            reverse('check_payment_status', 
                   kwargs={'request_number': self.service_request.request_number})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'is_paid': False,
                'status': 'pending'
            }
        )