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
    # saved_by = models.ManyToManyField(User, related_name='saved_journals', blank=True)
    souvenir = models.ForeignKey('Souvenir', on_delete=models.SET_NULL, null=True, blank=True)  # Relasi dengan Souvenir

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return user in self.likes.all()

class Souvenir(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()  # Rating antara 1.0 hingga 5.0
    description = models.TextField()
