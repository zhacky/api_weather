from django.db import models


# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
    images = models.Manager()
