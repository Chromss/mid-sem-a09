from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from places.views import CustomLoginView
from django.contrib.auth import views as auth_views

from main.views import (
    landing_page, journal_home, create_journal, edit_journal, delete_journal, journal_history,
    like_journal, journal_detail, register, login_user, logout_user, specific_journal, save_journal, logout, souvenir_list, itinerary_list, itinerary_detail, login, logout, 
    show_xml, show_xml_by_id, show_json, show_json_by_id,
    show_xml_itin, show_xml_by_id_itin, show_json_itin, show_json_by_id_itin,
    get_places, get_souvenirs, create_journal_flutter, get_journals_json,
)


app_name = 'main'

urlpatterns = [
    path('', landing_page, name='landing_page'),  # Halaman landing
    path('journal/', journal_home, name='journal_home'),
    path('create/', create_journal, name='create_journal'),
    path('edit/<int:journal_id>/', edit_journal, name='edit_journal'),
    path('delete/<int:journal_id>/', delete_journal, name='delete_journal'),
    path('journal_history/', journal_history, name='journal_history'), 
    path('like/<int:journal_id>/', like_journal, name='like_journal'),
    path('journal/<int:journal_id>/', journal_detail, name='journal_detail'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    # path('history/', user_history, name='user_history'),
    path('<int:journal_id>/', specific_journal, name='specific_journal'),
    path('save/<int:journal_id>/', save_journal, name='save_journal'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('souvenirs/', souvenir_list, name='souvenir_list'),
    path('itinerary/', itinerary_list, name='itinerary_list'),
    path('itinerary/<int:pk>/', itinerary_detail, name='itinerary_detail'),
    path('places/', include('places.urls')),  # namespace will be defined in places/urls.py
    # path('accounts/login/', CustomLoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),  # Remove admin namespace from here
    # path('placecollections/', include('placeCollection.urls')),  # namespace will be defined in placeCollection/urls.py
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('xmlitin/', show_xml_itin, name='show_xml_itin'),
    path('jsonitin/', show_json_itin, name='show_json_itin'),
    path('xmlitin/<str:id>/', show_xml_by_id_itin, name='show_xml_by_id_itin'),
    path('jsonitin/<str:id>/', show_json_by_id_itin, name='show_json_by_id_itin'),
    path('get-places/', get_places, name='get_places'),
    path('get-souvenirs/', get_souvenirs, name='get_souvenirs'),
    path('create-journal-flutter/', create_journal_flutter, name='create_journal_flutter'),
    # urls.py
    path('get-journals/', get_journals_json, name='get_journals_json'),

    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


