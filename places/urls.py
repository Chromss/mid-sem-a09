# places/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Remove or comment out the 'home' path
    # path('', views.home, name='home'),

    # Redirect root URL to a specific place detail
    path('', views.place_detail, {'place_id': 1}, name='home'),  # Replace '1' with a valid place_id
    path('<int:place_id>/', views.place_detail, name='place_detail'),
]
