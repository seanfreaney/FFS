from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
]
