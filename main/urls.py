from django.urls import path,include
from main.views import *

#new 
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from places.views import CustomLoginView
from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    path('', test, name='test_page'),
    path('landing-page/', landing_page, name='landing_page'),
    path('places/', include('places.urls')),
     # Authentication URLs
    path('accounts/login/', CustomLoginView.as_view(), name='login'),  # Custom login view
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Default logout view
    #admin
    path('admin/', admin.site.urls),
    path('placecollections/', include('placeCollection.urls')),
]