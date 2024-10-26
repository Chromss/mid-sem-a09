# models.py
from django.db import models
from places.models import Place

class PlaceCollection(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define AutoField
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    places = models.ManyToManyField(Place, related_name='collections')

    def __str__(self):
        return self.name