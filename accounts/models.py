from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=255, blank=True)
    birthday = models.CharField(max_length=100, blank=True, null=True)

    summary = models.TextField(blank=True)

    domain = models.CharField(max_length=255, blank=True)
    field = models.CharField(max_length=255, blank=True)

    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    work = models.CharField(max_length=255, blank=True)
    education = models.CharField(max_length=255, blank=True)

    skills = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
