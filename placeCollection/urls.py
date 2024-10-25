# urls.py (di dalam folder aplikasi)
from django.urls import path
from . import views

app_name = 'placeCollection'

urlpatterns = [
    path('show-collections/', views.show_collections, name='show_collections'),
]
