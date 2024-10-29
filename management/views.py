from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def management_dashboard(request):
    return render(request, 'management/management_dashboard.html')