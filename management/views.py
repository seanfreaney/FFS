from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from service_requests.models import ServiceRequest, Document, STATUS_CHOICES

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

@staff_member_required
def service_request_detail(request, request_number):
    service_request = get_object_or_404(ServiceRequest, request_number=request_number)
    documents = service_request.documents.all()

    if request.method == 'POST':
        # Update status and quote amount
        status = request.POST.get('status')
        quote_amount = request.POST.get('quote_amount')
        
        if status and status in dict(STATUS_CHOICES):
            service_request.status = status
        
        if quote_amount:
            try:
                service_request.quote_amount = float(quote_amount)
            except ValueError:
                messages.error(request, 'Invalid quote amount provided.')
                return redirect('management:service_request_detail', request_number=request_number)
        
        service_request.save()
        messages.success(request, 'Service request updated successfully.')
        return redirect('management:service_request_detail', request_number=request_number)

    context = {
        'service_request': service_request,
        'documents': documents,
    }
    return render(request, 'management/service_request_detail.html', context)

@staff_member_required
def upload_owner_document(request, request_number):
    service_request = get_object_or_404(ServiceRequest, request_number=request_number)
    
    if request.method == 'POST' and request.FILES.get('file'):
        document = Document.objects.create(
            service_request=service_request,
            file=request.FILES['file'],
            uploaded_by=request.user,
            document_type='owner',
            is_bank_statement=False  # Or add a field in the form to specify this
        )
        messages.success(request, 'Document uploaded successfully.')
    else:
        messages.error(request, 'Please select a file to upload.')
    
    return redirect('management:service_request_detail', request_number=request_number)