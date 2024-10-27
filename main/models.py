from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinLengthValidator
from django.db import models
import uuid

class MlakuMlakuUser(AbstractUser):
    name = models.CharField(max_length=25, validators=[MinLengthValidator(5)])
    username = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(5)])
    profile_picture = models.ImageField(upload_to='', default='static/img/noneicon.png')
    password = models.CharField(max_length=40, validators=[MinLengthValidator(10)])
    is_google = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(Group, related_name='mlakumlakuuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='mlakumlakuuser_set', blank=True)

    def __str__(self):
        return self.username