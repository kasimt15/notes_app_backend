from django.db import models

# Create your models here.
class Note(models.Model):
    title =models.CharField(max_length=200)
    body = models.TextField()
    #reated_at = models.DateTimeField(auto_now_add=True)
    #pdated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title