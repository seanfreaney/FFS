from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from service_requests.models import ServiceRequest

@staff_member_required
def management_dashboard(request):
    pending_count = ServiceRequest.objects.filter(status='pending').count()
    in_progress_count = ServiceRequest.objects.filter(status='in_progress').count()
    completed_count = ServiceRequest.objects.filter(status='completed').count()
    
    context = {
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    }
    return render(request, 'management/management_dashboard.html', context)

@staff_member_required
def service_request_management(request):
    service_requests = ServiceRequest.objects.all().order_by('-created_on')
    context = {
        'service_requests': service_requests,
    }
    return render(request, 'management/service_request_management.html', context)