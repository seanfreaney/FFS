from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceRequest, Document
from .forms import ServiceRequestForm, DocumentForm
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

PAYMENT_SUCCESS_MESSAGE = "Payment processed successfully! Your service request is now in progress."
PAYMENT_PROCESSING_MESSAGE = "Payment is being processed. Please wait for confirmation."
PAYMENT_ERROR_MESSAGE = "Payment failed: {error}. Please try again or contact support."

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
    service_request = get_object_or_404(
        ServiceRequest,
        request_number=request_number,
        user=request.user
    )
    
    # Debug print
    print(f"Service Request Status - is_paid: {service_request.is_paid}, status: {service_request.status}")
    
    context = {
        'service_request': service_request,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'service_requests/service_request_detail.html', context)

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

@login_required
def create_payment_intent(request, request_number):
    service_request = get_object_or_404(
        ServiceRequest, 
        request_number=request_number,
        user=request.user,
        quote_status='accepted',
        is_paid=False
    )
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(service_request.quote_amount * 100),
            currency=settings.STRIPE_CURRENCY,
            metadata={
                'request_number': str(service_request.request_number)
            }
        )
        
        service_request.stripe_payment_intent_id = intent.id
        service_request.save()
        
        return JsonResponse({
            'clientSecret': intent.client_secret,
            'requestNumber': service_request.request_number,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

@login_required
def payment_success(request, request_number):
    service_request = get_object_or_404(
        ServiceRequest,
        request_number=request_number,
        user=request.user
    )
    
    if service_request.is_paid:
        messages.success(request, "Payment confirmed! Your service request is now in progress.")
    else:
        messages.info(request, "Payment received! Please wait while we process your request.")
    
    return redirect('service_request_detail', request_number=request_number)

@login_required
def check_payment_status(request, request_number):
    service_request = get_object_or_404(
        ServiceRequest,
        request_number=request_number,
        user=request.user
    )
    return JsonResponse({
        'is_paid': service_request.is_paid,
        'status': service_request.status
    })

@login_required
def delete_service_request(request, request_number):
    service_request = get_object_or_404(ServiceRequest, request_number=request_number)
    
    # Check if user owns the request or is staff
    if request.user == service_request.user or request.user.is_staff:
        service_request.delete()
        messages.success(request, 'Service request successfully deleted.')
        return redirect('service_request_list')
    else:
        messages.error(request, 'You do not have permission to delete this request.')
        return redirect('service_request_list')