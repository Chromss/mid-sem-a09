# places/urls.py
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from . import flutter_api_views


app_name = 'places' 

urlpatterns = [
    # Remove or comment out the 'home' path
    # path('', views.home, name='home'),

    # Redirect root URL to a specific place detail
    path('', views.place_detail, {'place_id': 1}, name='home'),  # Replace '1' with a valid place_id
    path('<int:place_id>/', views.place_detail, name='place_detail'),
    path('add_comment/<int:place_id>/', views.add_comment_ajax, name='add_comment_ajax'),
    # path('comment/add/<int:place_id>/', views.add_comment_ajax, name='add_comment_ajax'),
    path('comment/edit/<int:comment_id>/', views.edit_comment_ajax, name='edit_comment_ajax'),
    path('comment/delete/<int:comment_id>/', views.delete_comment_ajax, name='delete_comment_ajax'),
    path('place/<int:place_id>/add_to_collection/', views.add_to_collection_ajax, name='add_to_collection_ajax'),
    path('buy/<int:souvenir_id>/', views.buy_souvenir_ajax, name='buy_souvenir_ajax'),
    path('<int:place_id>/json/', views.place_detail_json, name='place_detail_json'),
    path('flutter/add_comment/<int:place_id>/', 
         flutter_api_views.add_comment_flutter, 
         name='flutter_add_comment'),
    path('flutter/edit_comment/<int:comment_id>/', 
         flutter_api_views.edit_comment_flutter, 
         name='flutter_edit_comment'),
    path('flutter/delete_comment/<int:comment_id>/', 
         flutter_api_views.delete_comment_flutter, 
         name='flutter_delete_comment'),
    path('flutter/buy_souvenir/<int:souvenir_id>/', 
         flutter_api_views.buy_souvenir_flutter, 
         name='flutter_buy_souvenir'),
]
    # path('add-comment-dart/<int:place_id>/', views.add_comment_dart, name='add_comment_dart'),

# urlpatterns = [
#     path('', views.place_detail, {'place_id': 1}, name='home'),  # Replace '1' with a valid place_id
#     path('<int:place_id>/', views.place_detail, name='place_detail'),
#     path('api/add_comment/<int:place_id>/', views.add_comment_ajax, name='add_comment_ajax'),
#     path('api/comment/edit/<int:comment_id>/', views.edit_comment_ajax, name='edit_comment_ajax'),
#     path('api/comment/delete/<int:comment_id>/', views.delete_comment_ajax, name='delete_comment_ajax'),
#     path('api/place/<int:place_id>/add_to_collection/', views.add_to_collection_ajax, name='add_to_collection_ajax'),
#     path('api/buy/<int:souvenir_id>/', views.buy_souvenir_ajax, name='buy_souvenir_ajax'),
#     path('api/<int:place_id>/json/', views.place_detail_json, name='place_detail_json'),
#     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Endpoint to obtain token
# ]


#     path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
#     path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

