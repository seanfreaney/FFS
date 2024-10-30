from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from service_requests.models import ServiceRequest
from django.db.models import Count, Q

@staff_member_required
def management_dashboard(request):
    # Get counts for different service request statuses
    pending_count = ServiceRequest.objects.filter(status='pending').count()
    in_progress_count = ServiceRequest.objects.filter(status='in_progress').count()
    completed_count = ServiceRequest.objects.filter(status='completed').count()
    
    context = {
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    }
    return render(request, 'management/management_dashboard.html', context)