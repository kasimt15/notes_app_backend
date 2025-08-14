from django.contrib import admin
from .models import Note, UserProfile
# Register your models here.

admin.site.register(Note)
admin.site.register(UserProfile)