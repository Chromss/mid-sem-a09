from django import forms
from django.forms import ModelForm, TextInput
from .models import PlaceCollection

class CollectionForm(ModelForm):
    class Meta:
        model = PlaceCollection  # Pastikan model yang benar
        fields = ['name']  # Field yang ada di model
        labels = {
            'name': 'Collection Name'  # Label untuk field name
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter collection name'})
        }
