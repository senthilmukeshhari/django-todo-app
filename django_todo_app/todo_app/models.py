from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_img = models.ImageField(upload_to='profile_images', blank=False, null=False, default='profile_images/default_user.png')


class TodoList(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    is_completed = models.BooleanField(null=False, blank=False, default=0)

    def __str__(self):
        return str(self.username)