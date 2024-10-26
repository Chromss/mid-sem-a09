# models.py
from django.db import models

class Place(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class PlaceCollection(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define AutoField
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    places = models.ManyToManyField(Place, related_name='collections')

    def __str__(self):
        return self.name