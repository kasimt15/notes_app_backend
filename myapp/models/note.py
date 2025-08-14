from django.db import models
from django.contrib.auth.models import User
from .user_profile import UserProfile

# Create your models here.
class Note(models.Model):
    id= models.AutoField(primary_key=True)
    title =models.CharField(max_length=200)
    body = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notes')
    
    #reated_at = models.DateTimeField(auto_now_add=True)
    #pdated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    