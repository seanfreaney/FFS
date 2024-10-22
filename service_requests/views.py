from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest, Document
from .forms import ServiceRequestForm, DocumentForm


@login_required
def create_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES)
        if form.is_valid() and document_form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.status = 'pending'
            service_request.save()
            
            document = document_form.save(commit=False)
            document.service_request = service_request
            document.uploaded_by = request.user
            document.save()
            
            return redirect('service_request_detail', request_number=service_request.request_number)
    else:
        form = ServiceRequestForm()
        document_form = DocumentForm()
    return render(request, 'service_requests/create_service_request.html', {'form': form, 'document_form': document_form})

@login_required
def service_request_detail(request, request_number):
    service_request = get_object_or_404(ServiceRequest, request_number=request_number, user=request.user)
    documents = service_request.documents.all()
    return render(request, 'service_requests/service_request_detail.html', {'service_request': service_request, 'documents': documents})

@login_required
def service_request_list(request):
    service_requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'service_requests/service_request_list.html', {'service_requests': service_requests})
