from django.db import models

# Create your models here.


class Resume(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100, blank=True, null=True)
    skills = models.JSONField(default=dict)
    experience = models.JSONField(default=list)
    education = models.JSONField(default=list)
    projects = models.JSONField(default=list, blank=True, null=True)
    certifications = models.JSONField(default=list, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)