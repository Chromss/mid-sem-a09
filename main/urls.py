from django.urls import path
from main.views import test, landing_page, itinerary_list, itinerary_detail  # Import semua fungsi

app_name = 'main'

urlpatterns = [
    path('', test, name='test_page'),
    path('landing-page/', landing_page, name='landing_page'),
    path('itinerary/', itinerary_list, name='itinerary_list'),
    path('itinerary/<int:pk>/', itinerary_detail, name='itinerary_detail'),
]

# from django.urls import path
# from . import views

# app_name = 'main'

# urlpatterns = [
#     path('itineraries/', views.itinerary_list, name='itinerary_list'),
#     path('itineraries/<int:pk>/', views.itinerary_detail, name='itinerary_detail'),
# ]
