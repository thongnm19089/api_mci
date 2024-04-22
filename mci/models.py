from django.db import models 
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    hometown = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100, blank=True)
    avatar = models.TextField(max_length=100,null=True, blank=True)
   
class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ManyToManyField(UserProfile, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField( max_length=100)