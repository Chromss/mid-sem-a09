# urls.py
from django.urls import path
from . import views

app_name = 'placeCollection'

urlpatterns = [
    path('show-collections/', views.show_collections, name='show_collections'),
    path('create/', views.create_collection, name='create_collection'),
    path('create_collection_json/', views.create_collection_json, name='create_collection_json'),
    path('<int:collection_id>/places/', views.show_collection_places, name='show_collection_places'),
    path('delete/<int:collection_id>/', views.delete_collection, name='delete_collection'),
    path('<int:collection_id>/places/json/', views.show_json_collection_places, name='show_json_collection_places'),  # New endpoint
    # path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    # path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    # path('places-json/', views.show_collection_places, name='show_json_collection_places'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),

]
