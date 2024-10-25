from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('placecollections/', include('placecollections.urls', namespace='placecollections')),
    path('', include('placeCollection.urls', namespace='placeCollection')),
]