from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class ManagementViewsTest(TestCase):
    def setUp(self):
        # Create a staff user
        User = get_user_model()
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpass123',
            is_staff=True
        )
        
        # Create a regular user
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpass123'
        )
        
        # Set up the test client
        self.client = Client()

    def test_management_dashboard_view(self):
        # Test access denied for non-staff
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.get(reverse('management:management_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

        # Test access granted for staff
        self.client.login(username='staffuser', password='testpass123')
        response = self.client.get(reverse('management:management_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/management_dashboard.html')