from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from places.views import CustomLoginView
from django.contrib.auth import views as auth_views
from main.views import test, landing_page

# Remove app_name = 'main' from here since this is the root URLconf

urlpatterns = [
    path('', test, name='test_page'),
    path('landing-page/', landing_page, name='landing_page'),
    path('places/', include('places.urls')),  # namespace will be defined in places/urls.py
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),  # Remove admin namespace from here
    # path('placecollections/', include('placeCollection.urls')),  # namespace will be defined in placeCollection/urls.py
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)