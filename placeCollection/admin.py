from django.contrib import admin
from .models import Collection

@admin.register(Collection)
class PlaceCollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
