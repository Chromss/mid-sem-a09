# from django.db import models

# # Create your models here.
# from django.db import models
# import uuid

# class Place(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()

#     def __str__(self):
#         return self.title


# class PlaceCollection(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     places = models.ManyToManyField(Place)
#     progress = models.IntegerField(default=0)

#     def __str__(self):
#         return self.name

#BEFORE
# from django.db import models
# from django.utils import timezone


# class Collection(models.Model):
#     name = models.CharField(max_length=20)
#     created_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.name
    
#AFTER
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from places.models import Place

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    places = models.ManyToManyField('places.Place', through='CollectionItem', related_name='collections')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class CollectionItem(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='collection_items')

    class Meta:
        unique_together = ('collection', 'place')

    def __str__(self):
        return f"{self.place.name} in {self.collection.name}"

