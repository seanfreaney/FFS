from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

            messages.success(request, f"Service request #{service_request.request_number} has been successfully submitted.")
            
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

@login_required
def edit_service_request(request, request_number):
    service_request = get_object_or_404(ServiceRequest, request_number=request_number, user=request.user)
    document = service_request.documents.first()  # Assuming one document per request

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, instance=service_request)
        document_form = DocumentForm(request.POST, request.FILES, instance=document)
        
        if form.is_valid() and document_form.is_valid():
            form.save()
            if document:
                document_form.save()
            else:
                new_document = document_form.save(commit=False)
                new_document.service_request = service_request
                new_document.uploaded_by = request.user
                new_document.save()
            
            messages.success(request, 'Service request updated successfully.')
            return redirect('service_request_detail', request_number=service_request.request_number)
    else:
        form = ServiceRequestForm(instance=service_request)
        document_form = DocumentForm(instance=document)
    
    return render(request, 'service_requests/edit_service_request.html', {
        'form': form,
        'document_form': document_form,
        'service_request': service_request
    })

@login_required
def quote_response(request, request_number):
    service_request = get_object_or_404(ServiceRequest, request_number=request_number, user=request.user)
    
    if request.method == 'POST' and service_request.quote_status == 'pending':
        response = request.POST.get('response')
        if response in ['accepted', 'rejected']:
            service_request.quote_status = response
            if response == 'accepted':
                service_request.status = 'in_progress'
            service_request.save()
            messages.success(request, f'Quote has been {response}.')
        else:
            messages.error(request, 'Invalid response.')
    
    return redirect('service_request_detail', request_number=request_number)
