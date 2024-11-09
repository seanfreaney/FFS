from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('create/', views.create_service_request, name='create_service_request'),
    path('list/', views.service_request_list, name='service_request_list'),
    path('<uuid:request_number>/', views.service_request_detail, name='service_request_detail'),
    path('edit/<uuid:request_number>/', views.edit_service_request, name='edit_service_request'),
    path('<uuid:request_number>/quote-response/', views.quote_response, name='quote_response'),
    path('request/<uuid:request_number>/create-payment-intent/', 
         views.create_payment_intent, 
         name='create_payment_intent'),
    path('<uuid:request_number>/payment-success/', 
         views.payment_success, 
         name='payment_success'),
    path('webhook/stripe/', webhook, name='webhook'),
    path('request/<uuid:request_number>/check-payment-status/', 
         views.check_payment_status, 
         name='check_payment_status'),
    path('request/<uuid:request_number>/delete/', 
         views.delete_service_request, 
         name='delete_service_request'),
]

