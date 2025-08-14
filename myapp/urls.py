from django.http import HttpResponse
from django.urls import path
from . import views
urlpatterns = [
    path('create/note/', views.addNoteToModelAPI),
    path('create/user/',views.addUserToModelAPI),
    path('edit/note/', views.updateNoteToModelAPI)
]
