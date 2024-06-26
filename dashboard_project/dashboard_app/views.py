from django.http import JsonResponse
from dashboard_app.models import DataEntry
from django.shortcuts import render

def get_data(request):
    entries = DataEntry.objects.all().values()
    return JsonResponse(list(entries), safe=False)

def index(request):
    return render(request, 'dashboard_app/index.html')
