from admin_only.views import *
from django.urls import path

app_name = 'admin_only'

urlpatterns = [
    path('assign/', assign, name='assign'),
    path('login/', login_admin, name='login_admin'),
    path('logout/', logout_admin, name='logout_admin'),
    path('create-place/', create_place, name='create_place'),
    path('create-souvenir/', create_souvenir, name='create_souvenir'),
    path('show-places/', show_places, name='show_places'),
    path('update-place/<int:place_id>/', update_place, name='update_place'),
    path('delete-place/<int:place_id>/', delete_place, name='delete_place'),
    path('json-place/', show_json_place, name='show_json_place'),
    path('json-souvenir/', show_json_souvenir, name='show_json_souvenir'),
]