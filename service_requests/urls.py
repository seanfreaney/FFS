from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_service_request, name='create_service_request'),
    path('list/', views.service_request_list, name='service_request_list'),
    path('<uuid:request_number>/', views.service_request_detail, name='service_request_detail'),
]

