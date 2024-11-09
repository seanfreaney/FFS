from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NewsletterSubscriber

# Create your views here.

def index(request):
    """ View to return the index page"""

    return render(request, 'home/index.html')


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Check if email already exists
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, 'Successfully subscribed to newsletter!')
            else:
                messages.info(request, 'You are already subscribed!')
        return redirect(request.META.get('HTTP_REFERER', '/'))