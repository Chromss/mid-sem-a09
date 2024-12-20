import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Journal(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journals')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='journal_images/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_journals', blank=True)
    souvenir = models.ForeignKey('Souvenir', on_delete=models.SET_NULL, null=True, blank=True)
    place_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return user in self.likes.all()

class Souvenir(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    place_name = models.CharField(max_length=200)  # 
    description = models.TextField()

# Model untuk Itinerary
class Itinerary(models.Model):
    name = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='trip_covers/', blank=True, null=True)

    def __str__(self):
        return self.name

# Model untuk Hari dalam Itinerary
class Day(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name='days', on_delete=models.CASCADE)
    day_number = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"Day {self.day_number} - {self.date}"

# Model untuk Destinasi dalam Hari
class Destination(models.Model):
    day = models.ForeignKey(Day, related_name='destinations', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} at {self.time}"


