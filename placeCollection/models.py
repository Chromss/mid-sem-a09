from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from places.models import Place


# Remove the duplicate Place model
# class Place(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#
#     def __str__(self):
#         return self.title

# Model untuk Collection dengan UUID sebagai primary key
class Collection(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define AutoField
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=255)  # Menggunakan max_length 255 seperti di PlaceCollection
    created_at = models.DateTimeField(auto_now_add=True)
    places = models.ManyToManyField(Place, through='CollectionItem', related_name='collections')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

# Intermediate model untuk relasi many-to-many Collection dan Place
class CollectionItem(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='collection_items')

    class Meta:
        unique_together = ('collection', 'place')

    def __str__(self):
        return f"{self.place.title} in {self.collection.name}"
