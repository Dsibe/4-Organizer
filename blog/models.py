from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200, blank=True)
    img_path = models.CharField(max_length=200,
                                blank=True,
                                default='placeholder.png')
    body = models.TextField(max_length=100_000, blank=True)
