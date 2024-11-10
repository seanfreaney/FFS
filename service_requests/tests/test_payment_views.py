from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from service_requests.models import ServiceRequest
from unittest.mock import patch
import uuid

class PaymentViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a service request with accepted quote
        self.service_request = ServiceRequest.objects.create(
            user=self.user,
            business_type='Test Business',
            monthly_revenue=1000.00,
            monthly_transactions=100,
            monthly_operating_costs=500.00,
            quote_amount=100.00,
            quote_status='accepted',
            status='pending',
            is_paid=False
        )

    @patch('stripe.PaymentIntent.create')
    def test_create_payment_intent_success(self, mock_create):
        # Mock the Stripe response
        mock_create.return_value = type('obj', (object,), {
            'client_secret': 'test_secret',
            'id': 'test_id'
        })

        # Log in the user
        self.client.force_login(self.user)

        # Make the request
        response = self.client.post(
            reverse('create_payment_intent', kwargs={'request_number': self.service_request.request_number})
        )

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertIn('clientSecret', response.json())
        self.assertIn('requestNumber', response.json())

        # Verify Stripe was called correctly
        mock_create.assert_called_once_with(
            amount=10000,  # 100.00 converted to cents
            currency='eur',
            metadata={'request_number': str(self.service_request.request_number)}
        )