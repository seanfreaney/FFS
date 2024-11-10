from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from service_requests.models import ServiceRequest
from unittest.mock import patch
import uuid
from django.contrib import messages
from django.contrib.messages import get_messages

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

    def test_create_payment_intent_unauthorized(self):
        response = self.client.post(
            reverse('create_payment_intent', args=[self.service_request.request_number])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_create_payment_intent_invalid_request(self):
        """Test payment intent creation with unpaid/unaccepted quote"""
        self.client.force_login(self.user)
        # Set quote status to pending
        self.service_request.quote_status = 'pending'
        self.service_request.save()
        
        response = self.client.post(
            reverse('create_payment_intent', args=[self.service_request.request_number])
        )
        self.assertEqual(response.status_code, 404)

    def test_payment_success_view(self):
        """Test the payment success view"""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('payment_success', args=[self.service_request.request_number])
        )
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(
            response,
            reverse('service_request_detail', args=[self.service_request.request_number])
        )

    def test_check_payment_status(self):
        """Test the payment status check endpoint"""
        self.client.force_login(self.user)
        
        # Initial state (not paid)
        response = self.client.get(
            reverse('check_payment_status', args=[self.service_request.request_number])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'is_paid': False,
            'status': 'pending'
        })
        
        # Update service request to paid
        self.service_request.mark_as_paid()
        
        # Check updated state
        response = self.client.get(
            reverse('check_payment_status', args=[self.service_request.request_number])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'is_paid': True,
            'status': 'in_progress'
        })

    def test_create_payment_intent_wrong_user(self):
        """Test creating payment intent for another user's service request"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.force_login(other_user)
        
        response = self.client.post(
            reverse('create_payment_intent', args=[self.service_request.request_number])
        )
        self.assertEqual(response.status_code, 404)

    def test_payment_success_not_paid(self):
        """Test payment success view when payment is not yet confirmed"""
        self.client.force_login(self.user)
        self.service_request.is_paid = False
        self.service_request.save()
        
        response = self.client.get(
            reverse('payment_success', args=[self.service_request.request_number])
        )
        
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Payment received! Please wait", str(messages[0]))

    def test_payment_success_already_paid(self):
        """Test payment success view when payment is already confirmed"""
        self.client.force_login(self.user)
        self.service_request.is_paid = True
        self.service_request.save()
        
        response = self.client.get(
            reverse('payment_success', args=[self.service_request.request_number])
        )
        
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Payment confirmed!", str(messages[0]))

    def test_check_payment_status_unauthorized(self):
        """Test check payment status with wrong user"""
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.client.force_login(other_user)
        
        response = self.client.get(
            reverse('check_payment_status', args=[self.service_request.request_number])
        )
        self.assertEqual(response.status_code, 404)

    def test_check_payment_status_nonexistent(self):
        """Test check payment status with non-existent request"""
        self.client.force_login(self.user)
        fake_uuid = uuid.uuid4()
        
        response = self.client.get(
            reverse('check_payment_status', args=[fake_uuid])
        )
        self.assertEqual(response.status_code, 404)

    