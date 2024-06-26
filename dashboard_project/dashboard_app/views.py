from django.http import JsonResponse
from dashboard_app.models import DataEntry
from django.shortcuts import render

def get_data(request):
    #entries = DataEntry.objects.all().values()
    entries = DataEntry.objects.all().values(
        'topic', 'intensity', 'sector', 'insight', 'url', 'region', 'country', 'relevance', 'pestle', 'source', 'title', 'likelihood'
    )

    return JsonResponse(list(entries), safe=False)

def index(request):
    return render(request, 'dashboard_app/index.html')
