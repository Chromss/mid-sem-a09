# places/models.py

from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='places/images/')

    def __str__(self):
        return self.name

class Souvenir(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='souvenirs')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='souvenirs/images/')

    def __str__(self):
        return self.name

class Comment(models.Model):
    PLACE_RATING_CHOICES = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]

    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=PLACE_RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.place.name} - {self.rating} Stars"

    class Meta:
        ordering = ['-created_at']
