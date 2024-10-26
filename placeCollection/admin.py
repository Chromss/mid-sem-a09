from django.contrib import admin
from .models import PlaceCollection

@admin.register(PlaceCollection)
class PlaceCollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
