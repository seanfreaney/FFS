from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.management_dashboard, name='management_dashboard'),
    path('service-requests/', views.service_request_management, name='service_request_management'),
]