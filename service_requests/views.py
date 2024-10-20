from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest
from .forms import ServiceRequestForm


@login_required
def create_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.status = 'pending'
            service_request.save()
            return redirect('service_request_detail', request_number=service_request.request_number)
    else:
        form = ServiceRequestForm()
    return render(request, 'service_requests/create_service_request.html', {'form': form})

@login_required
def service_request_detail(request, request_number):
    service_request = get_object_or_404(ServiceRequest, request_number=request_number, user=request.user)
    return render(request, 'service_requests/service_request_detail.html', {'service_request': service_request})

@login_required
def service_request_list(request):
    service_requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'service_requests/service_request_list.html', {'service_requests': service_requests})
