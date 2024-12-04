from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from places.views import CustomLoginView
from django.contrib.auth import views as auth_views
from main.views import landing_page

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include('admin_only.urls')),
    path('auth/', include('authentication.urls')),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('places/', include('places.urls')),  # Include places URLs
    # path('accounts/login/', CustomLoginView.as_view(), name='login'),  # Use custom login view
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'), ini dua yh
    # path('placecollections/', include('placeCollection.urls', namespace='placeCollection')),  # Tambahkan namespace jika dibutuhkan
    # path('show-collections/', include(('placeCollection.urls', 'placeCollection'), namespace='placeCollection')),
    # path('placeCollection/', include('placeCollection.urls')), 
    path('placeCollection/', include('placeCollection.urls', namespace='placeCollection')),
    path('', landing_page, name='landing_page'),  # Ini akan mengarahkan root URL ke landing page
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]