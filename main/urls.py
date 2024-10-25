from django.urls import path
from main.views import (
    journal_home, create_journal, edit_journal, delete_journal,
    like_journal, save_journal, journal_detail, register, login_user, logout_user, specific_journal, user_history
)

app_name = 'main'

urlpatterns = [
    path('', journal_home, name='journal_home'),
    path('create/', create_journal, name='create_journal'),
    path('edit/<int:journal_id>/', edit_journal, name='edit_journal'),
    path('delete/<int:journal_id>/', delete_journal, name='delete_journal'),
    path('like/<int:journal_id>/', like_journal, name='like_journal'),
    path('save/<int:journal_id>/', save_journal, name='save_journal'),
    path('journal/<int:journal_id>/', journal_detail, name='journal_detail'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('history/', user_history, name='user_history'),
    path('<int:journal_id>/', specific_journal, name='specific_journal')
]