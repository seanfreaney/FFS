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

    def test_service_request_detail_post(self):
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

        # Login as staff
        self.client.login(username='staffuser', password='testpass123')

        # Test valid status update
        response = self.client.post(
            reverse('management:service_request_detail', kwargs={'request_number': test_request.request_number}),
            {'status': 'in_progress', 'quote_amount': '2500.00'}
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify updates
        test_request.refresh_from_db()
        self.assertEqual(test_request.status, 'in_progress')
        self.assertEqual(test_request.quote_amount, 2500.00)

       # Test invalid quote amount
        response = self.client.post(
            reverse('management:service_request_detail', kwargs={'request_number': test_request.request_number}),
            {'status': 'completed', 'quote_amount': 'invalid'}
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify status didn't change due to invalid input
        test_request.refresh_from_db()
        self.assertEqual(test_request.status, 'in_progress')
        self.assertEqual(test_request.quote_amount, 2500.00)

        # Test with valid quote amount
        response = self.client.post(
            reverse('management:service_request_detail', kwargs={'request_number': test_request.request_number}),
            {'status': 'completed', 'quote_amount': '3000.00'}
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify both fields updated
        test_request.refresh_from_db()
        self.assertEqual(test_request.status, 'completed')
        self.assertEqual(test_request.quote_amount, 3000.00)

    def test_management_dashboard_counts(self):
        # Create multiple service requests with different statuses
        from service_requests.models import ServiceRequest
        
        # Create 2 pending requests
        ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='pending',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='Test Business 1',
            monthly_transactions=100,
            monthly_operating_costs=500.00
        )
        ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='pending',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='Test Business 2',
            monthly_transactions=100,
            monthly_operating_costs=500.00
        )
        
        # Create 1 in_progress request
        ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='in_progress',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='Test Business 3',
            monthly_transactions=100,
            monthly_operating_costs=500.00
        )
        
        # Create 1 completed request
        ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='completed',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='Test Business 4',
            monthly_transactions=100,
            monthly_operating_costs=500.00
        )

        # Login as staff and check the dashboard
        self.client.login(username='staffuser', password='testpass123')
        response = self.client.get(reverse('management:management_dashboard'))
        
        # Verify the counts in the context
        self.assertEqual(response.context['pending_count'], 2)
        self.assertEqual(response.context['in_progress_count'], 1)
        self.assertEqual(response.context['completed_count'], 1)

    def test_service_request_management_date_ordering(self):
        from service_requests.models import ServiceRequest
        from django.utils import timezone
        from datetime import timedelta
        
        # Create service requests with different dates
        old_date = timezone.now() - timedelta(days=7)
        mid_date = timezone.now() - timedelta(days=3)
        new_date = timezone.now()
        
        # Create requests with specific dates
        old_request = ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='pending',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='Old Request',
            monthly_transactions=100,
            monthly_operating_costs=500.00,
            created_on=old_date
        )
        
        mid_request = ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='pending',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='Mid Request',
            monthly_transactions=100,
            monthly_operating_costs=500.00,
            created_on=mid_date
        )
        
        new_request = ServiceRequest.objects.create(
            request_number=uuid.uuid4(),
            status='pending',
            monthly_revenue=1000.00,
            user=self.regular_user,
            business_type='New Request',
            monthly_transactions=100,
            monthly_operating_costs=500.00,
            created_on=new_date
        )

        self.client.login(username='staffuser', password='testpass123')
        
        # Test newest first (default)
        response = self.client.get(reverse('management:service_request_management'))
        requests = response.context['service_requests']
        self.assertEqual(requests[0], new_request)
        self.assertEqual(requests[2], old_request)
        
        # Test oldest first
        response = self.client.get(
            reverse('management:service_request_management'),
            {'date_order': 'oldest'}
        )
        requests = response.context['service_requests']
        self.assertEqual(requests[0], old_request)
        self.assertEqual(requests[2], new_request)
        
        # Test newest first (explicit)
        response = self.client.get(
            reverse('management:service_request_management'),
            {'date_order': 'newest'}
        )
        requests = response.context['service_requests']
        self.assertEqual(requests[0], new_request)
        self.assertEqual(requests[2], old_request)