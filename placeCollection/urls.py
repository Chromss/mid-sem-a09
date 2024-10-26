from django.urls import path
from . import views

app_name = 'placeCollection'  # Define namespace here

urlpatterns = [
    path('', views.show_collections, name='show_collections'),
    path('create/', views.create_collection, name='create_collection'),
    path('<int:collection_id>/places/', views.show_collection_places, name='show_collection_places'),
]