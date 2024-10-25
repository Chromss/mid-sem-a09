import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# class Journal(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journals')
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     image = models.ImageField(upload_to='journal_images/', null=True, blank=True)
#     likes = models.ManyToManyField(User, related_name='liked_journals', blank=True)
#     saved_by = models.ManyToManyField(User, related_name='saved_journals', blank=True)

#     def __str__(self):
#         return self.title

#     def total_likes(self):
#         return self.likes.count()

#     def is_liked_by(self, user):
#         return user in self.likes.all()

#     def is_saved_by(self, user):
#         return user in self.saved_by.all()

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='journal_images/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    journal = models.ForeignKey(Journal, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("journal", "user")

class SavedJournal(models.Model):
    journal = models.ForeignKey(Journal, related_name="saved_journals", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("journal", "user")

