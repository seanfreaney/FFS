from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid

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

    def test_service_request_management_view(self):
        # Create some test service requests
        from service_requests.models import ServiceRequest
        
        ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='pending',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='Test Business',
            monthly_transactions=100,
            monthly_operating_costs=500.00
        )
        ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='completed',
            monthly_revenue=2000.00,
            user=self.regular_user,
            business_type='Test Business 2',
            monthly_transactions=200,
            monthly_operating_costs=1000.00
        )

        # Test access denied for non-staff
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.get(reverse('management:service_request_management'))
        self.assertEqual(response.status_code, 302)  # Should redirect

        # Login as staff
        self.client.login(username='staffuser', password='testpass123')
        
        # Test basic list view
        response = self.client.get(reverse('management:service_request_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/service_request_management.html')
        self.assertEqual(len(response.context['service_requests']), 2)

        # Test status filter
        response = self.client.get(
            reverse('management:service_request_management'),
            {'status': 'pending'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['service_requests']), 1)
        self.assertEqual(response.context['service_requests'][0].status, 'pending')
    
    def test_service_request_detail_view(self):
        # Create a test service request
        from service_requests.models import ServiceRequest
        
        test_request = ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='pending',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='Test Business',
            monthly_transactions=100,
            monthly_operating_costs=500.00
        )

        # Test access denied for non-staff
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.get(reverse('management:service_request_detail', 
            kwargs={'request_number': test_request.request_number}))
        self.assertEqual(response.status_code, 302)  # Should redirect

        # Test access granted for staff
        self.client.login(username='staffuser', password='testpass123')
        response = self.client.get(reverse('management:service_request_detail', 
            kwargs={'request_number': test_request.request_number}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management/service_request_detail.html')
        
        # Verify context data
        self.assertEqual(response.context['service_request'], test_request)

    def test_upload_owner_document_view(self):
        # Create a test service request
        from service_requests.models import ServiceRequest
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        test_request = ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='pending',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='Test Business',
            monthly_transactions=100,
            monthly_operating_costs=500.00
        )

        # Create a test file
        test_file = SimpleUploadedFile(
            "test_document.pdf",
            b"file_content",
            content_type="application/pdf"
        )

        # Test access denied for non-staff
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.post(
            reverse('management:upload_owner_document', kwargs={'request_number': test_request.request_number}),
            {'file': test_file}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to login

        # Test successful upload for staff
        self.client.login(username='staffuser', password='testpass123')
        response = self.client.post(
            reverse('management:upload_owner_document', kwargs={'request_number': test_request.request_number}),
            {'file': test_file}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to detail page
        
        # Verify document was created
        self.assertTrue(test_request.documents.filter(document_type='owner').exists())
        
        # Test upload without file
        response = self.client.post(
            reverse('management:upload_owner_document', kwargs={'request_number': test_request.request_number}),
            {}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to detail page