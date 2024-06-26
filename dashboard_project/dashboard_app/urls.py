from django.urls import path
from .views import get_data, index


urlpatterns = [
    path('', index, name='index'),
    path('api/data/', get_data, name='get_data')
]
