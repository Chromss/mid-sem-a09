from django.urls import path
from main.views import *
from django.urls import path, include

app_name = 'main'

urlpatterns = [
    path('', test, name='test_page'),
    path('landing-page/', landing_page, name='landing_page'),
    path('placecollections/', include('placeCollection.urls')),
]