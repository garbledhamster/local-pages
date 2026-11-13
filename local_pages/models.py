from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=63, unique=True)
    provider = models.CharField(max_length=12)
    repository = models.CharField(max_length=500)
    branch = models.CharField(max_length=250)
    folder = models.CharField(max_length=400)
    entry = models.CharField(max_length=400)
    credential = models.TextField(blank=True)
    revision = models.CharField(max_length=64)
    snapshot = models.UUIDField()
