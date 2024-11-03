from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.management_dashboard, name='management_dashboard'),
    path('service-requests/', views.service_request_management, name='service_request_management'),
    path('service-requests/<uuid:request_number>/', views.service_request_detail, name='service_request_detail'),
    path('service-requests/<uuid:request_number>/upload-document/', 
         views.upload_owner_document, 
         name='upload_owner_document'),
]