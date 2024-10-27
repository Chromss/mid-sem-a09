from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup/next/', signup_next, name='signup_next'),
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('about/', about, name='about'),
    path('xml/', show_xml, name='show_xml'),
    
]