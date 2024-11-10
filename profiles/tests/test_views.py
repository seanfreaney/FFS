from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile
from service_requests.models import ServiceRequest

class TestProfileView(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profile = UserProfile.objects.get(user=self.user)
        self.url = reverse('profile')

    def test_profile_view_redirect_if_not_logged_in(self):
        """Test profile view redirects if user is not logged in"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_view_GET(self):
        """Test GET request to profile view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertTrue('form' in response.context)
        self.assertTrue('service_requests' in response.context)

    def test_profile_view_POST_valid_data(self):
        """Test POST request with valid form data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {
            'default_phone_number': '1234567890',
            'default_postcode': '12345',
            'default_town_or_city': 'Test City',
            'default_street_address1': 'Test Street',
            'default_street_address2': 'Apt 123',
            'default_county': 'Test County',
        })
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Profile updated successfully')

    def test_profile_view_displays_service_requests(self):
        """Test that service requests are displayed in profile"""
        self.client.login(username='testuser', password='testpass123')
        # Create a test service request
        ServiceRequest.objects.create(
            user=self.user,
            business_type='Retail',
            monthly_revenue=5000.00,
            monthly_transactions=100,
            monthly_operating_costs=3000.00,
            status='pending',
            quote_status='pending'
        )
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['service_requests']), 1)

    def test_profile_view_POST_invalid_data(self):
        """Test POST request with invalid form data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {
            'default_phone_number': 'invalid' * 50,  # Too long for CharField(max_length=20)
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        
    def test_profile_view_POST_empty_data(self):
        """Test POST request with empty data (should be valid as all fields are optional)"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Profile updated successfully')

    def test_service_requests_ordered_by_created_on(self):
        """Test that service requests are displayed in correct order (newest first)"""
        self.client.login(username='testuser', password='testpass123')
        # Create multiple service requests with different dates
        ServiceRequest.objects.create(
            user=self.user,
            business_type='Retail',
            monthly_revenue=5000.00,
            monthly_transactions=100,
            monthly_operating_costs=3000.00,
            status='pending',
            quote_status='pending'
        )
        ServiceRequest.objects.create(
            user=self.user,
            business_type='Service',
            monthly_revenue=5000.00,
            monthly_transactions=100,
            monthly_operating_costs=3000.00,
            status='pending',
            quote_status='pending'
        )
        response = self.client.get(self.url)
        requests = response.context['service_requests']
        self.assertTrue(requests[0].created_on > requests[1].created_on)
    
    def test_on_profile_page_context(self):
        """Test that on_profile_page context is True"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertTrue(response.context['on_profile_page'])

    def test_profile_view_with_no_service_requests(self):
        """Test profile view when user has no service requests"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['service_requests']), 0)