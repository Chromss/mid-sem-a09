from django import forms
from .models import PlaceCollection

class CollectionForm(forms.ModelForm):
    class Meta:
        model = PlaceCollection
        fields = ['name']  # Only the name field for now
