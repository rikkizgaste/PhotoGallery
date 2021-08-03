from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Album(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.description

