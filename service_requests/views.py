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
    
    # Add debug prints
    print(f"Stripe Public Key: {settings.STRIPE_PUBLIC_KEY}")
    print(f"Service Request Quote Amount: {service_request.quote_amount}")
    print(f"Service Request Status - is_paid: {service_request.is_paid}, status: {service_request.status}")
    
    context = {
        'service_request': service_request,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': '',
    }
    
    # Generate client secret if payment is needed
    if service_request.quote_status == 'accepted' and not service_request.is_paid:
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(service_request.quote_amount * 100),
                currency='eur',
                metadata={
                    'service_request_id': service_request.request_number
                }
            )
            context['client_secret'] = intent.client_secret
            print(f"Payment Intent Created: {intent.id}")
        except Exception as e:
            print(f"Error creating payment intent: {str(e)}")
            messages.error(request, "Unable to process payment at this time.")
    
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
    try:
        service_request = get_object_or_404(ServiceRequest, request_number=request_number)
        
        # Add debug prints
        print(f"Creating payment intent for request {request_number}")
        print(f"Amount: {service_request.quote_amount}")
        
        # Create the payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(service_request.quote_amount * 100),  # amount in cents
            currency='eur',
            metadata={
                'service_request_id': service_request.request_number
            }
        )
        
        print(f"Payment Intent Created Successfully: {intent.id}")
        
        return JsonResponse({
            'clientSecret': intent.client_secret,
            'requestNumber': service_request.request_number
        })
    except Exception as e:
        print(f'Payment Intent Error: {str(e)}')
        return JsonResponse({'error': str(e)}, status=400)  # Add status code

@login_required
def payment_success(request, request_number):
    service_request = get_object_or_404(
        ServiceRequest,
        request_number=request_number,
        user=request.user
    )
    
    # Add debug prints
    print(f"Payment Success Handler - Request {request_number}")
    print(f"Current status: is_paid={service_request.is_paid}, status={service_request.status}")
    
    if not service_request.is_paid:
        service_request.is_paid = True
        service_request.status = 'in_progress'
        service_request.save()
        print("Updated service request status to paid and in_progress")
    
    if service_request.is_paid:
        messages.success(request, PAYMENT_SUCCESS_MESSAGE)
    else:
        messages.info(request, PAYMENT_PROCESSING_MESSAGE)
    
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
    if request.user != service_request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this request.')
        return redirect('service_request_list')
    
    # Handle the deletion confirmation
    if request.method == 'POST':
        service_request.delete()
        messages.success(request, 'Service request successfully deleted.')
        return redirect('service_request_list')
        
    # If it's a GET request, show the confirmation page
    context = {
        'service_request': service_request,
    }
    return render(request, 'service_requests/request_confirm_delete.html', context)