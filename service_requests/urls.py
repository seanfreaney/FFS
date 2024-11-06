from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_service_request, name='create_service_request'),
    path('list/', views.service_request_list, name='service_request_list'),
    path('<uuid:request_number>/', views.service_request_detail, name='service_request_detail'),
    path('edit/<uuid:request_number>/', views.edit_service_request, name='edit_service_request'),
    path('<uuid:request_number>/quote-response/', views.quote_response, name='quote_response'),
    path('request/<uuid:request_number>/create-payment-intent/', 
         views.create_payment_intent, 
         name='create_payment_intent'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('<uuid:request_number>/payment-success/', 
         views.payment_success, 
         name='payment_success'),
]

