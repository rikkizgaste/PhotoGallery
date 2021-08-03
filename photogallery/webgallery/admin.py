from django.contrib import admin

# Register your models here.

from .models import Album, Image

admin.site.register(Album)
admin.site.register(Image)

