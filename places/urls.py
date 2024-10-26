# places/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Remove or comment out the 'home' path
    # path('', views.home, name='home'),

    # Redirect root URL to a specific place detail
    path('', views.place_detail, {'place_id': 1}, name='home'),  # Replace '1' with a valid place_id
    path('<int:place_id>/', views.place_detail, name='place_detail'),
    path('comment/add/<int:place_id>/', views.add_comment_ajax, name='add_comment_ajax'),
    path('comment/edit/<int:comment_id>/', views.edit_comment_ajax, name='edit_comment_ajax'),
    path('comment/delete/<int:comment_id>/', views.delete_comment_ajax, name='delete_comment_ajax'),
    path('place/<int:place_id>/add_to_collection/', views.add_to_collection_ajax, name='add_to_collection_ajax'),
    path('buy/<int:souvenir_id>/', views.buy_souvenir_ajax, name='buy_souvenir_ajax'),


#     path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
#     path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
