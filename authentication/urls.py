from django.urls import path
from authentication.views import login

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    # path('register/', register, name='register'),
    # path('logout/', logout, name='logout'),
]