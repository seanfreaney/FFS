from django.http import HttpResponse
from .models import ServiceRequest
from django.contrib import messages

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        request_number = intent.metadata.request_number
        
        try:
            service_request = ServiceRequest.objects.get(
                request_number=request_number,
                stripe_payment_intent_id=intent.id
            )
            
            # Use the helper method
            service_request.mark_as_paid()
            
            print(f"Payment confirmed for request {request_number}")  # Debug print
            
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Payment confirmed',
                status=200)
                
        except ServiceRequest.DoesNotExist:
            print(f"Service request not found: {request_number}")  # Debug print
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Service request not found',
                status=404)
                
        except Exception as e:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {str(e)}',
                status=500)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
