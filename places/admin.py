# places/admin.py

from django.contrib import admin
from .models import Place, Souvenir, Comment

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Souvenir)
class SouvenirAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'place')
    list_filter = ('place',)
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'content')
