from rest_framework import generics
from rest_framework.decorators import api_view


from django.http import HttpResponse
from django.shortcuts import render
from .models import Note, UserProfile
from .serializers import UserProfileSerializer, NoteSerializer
from firebase_admin import auth

from django.contrib.auth import get_user_model
user= get_user_model()

# Create your views here.
#API for adding Note to model
@api_view(['POST'])
def addNoteToModelAPI(request):
    id_token= request.data.get('id_token')
    if not id_token:
        print("No ID token provided")
        return HttpResponse("No ID token provided", status=400)
    
    try:
        decoded_token= auth.verify_id_token(id_token)
        uid= decoded_token.get('uid')
        user_profile_instance= UserProfile.objects.get(uid=uid)
        
        #copying the data from request body
        note_data= request.data.copy()
        note_data.pop('id_token', None)
        
        serializer= NoteSerializer(data= note_data)
        
        if serializer.is_valid():
            serializer.save(user= user_profile_instance)
            return HttpResponse(serializer.data, status=201)
        else:
            print(serializer.errors)
            return HttpResponse(serializer.errors, status= 400)
            
        
    except UserProfile.DoesNotExist:
        print({"detail": "User profile not found for provided ID token."})
        return HttpResponse({"detail": "User profile not found for provided ID token."}, status=404)
    except Exception as e:
        print({"detail": f"Error verifying ID token: {str(e)}"})
        return HttpResponse({"detail": f"Error verifying ID token: {str(e)}"}, status=400)

#API for adding user to model
@api_view(['POST'])
def addUserToModelAPI(request):
    id_token= request.data.get('id_token')
    if not id_token:
        return HttpResponse("No ID token provided", status=400)
    
    try:
        decoded_token= auth.verify_id_token(id_token)
        uid= decoded_token.get('uid')
        email= decoded_token.get('email')
        name= decoded_token.get('name')
        userJSON= {
            'uid': uid,
            'display_name': name,
            'email': email
        }
        userSerializer= UserProfileSerializer(data=userJSON)
        
        #checks if user exists in models
        if UserProfile.objects.filter(uid=uid).exists():
            print(f"{name} is here")
            return HttpResponse("User already exists!", status=200)
        
        #ensures that the request's content is valid
        if userSerializer.is_valid():
            userSerializer.save()
            return HttpResponse(userSerializer.data, status=201)
        else:
            print(userSerializer.errors) 
            return HttpResponse(userSerializer.errors, status= 400)
        
    except Exception as e:
        return HttpResponse(f"Error verifying ID token: {str(e)}", status=400)
    
#API for updating notes
@api_view(['PUT'])
def updateNoteToModelAPI(request):
    id_token= request.data.get('id_token')
    if not id_token:
        print("No ID token provided")
        return HttpResponse("No ID token provided", status=400)
    
    try:
        decoded_token= auth.verify_id_token(id_token)
        uid= decoded_token.get('uid')
        user_profile_instance= UserProfile.objects.get(uid=uid)
        
        #copying the data from request body
        note_data= request.data.copy()
        note_data.pop('id_token', None)
        
        #print(f"old title: {request.data.get('old_title')} \nold body: {request.data.get('old_body')}")
        note_to_update= Note.objects.get(title= note_data.get('old_title'), body= note_data.get('old_body'))
        note_data.pop('old_title', None)
        note_data.pop('old_body', None)
        
        serializer= NoteSerializer(note_to_update, data= note_data)
        
        if serializer.is_valid():
            serializer.save(user= user_profile_instance)
            return HttpResponse(serializer.data, status=201)
        else:
            print(serializer.errors)
            return HttpResponse(serializer.errors, status= 400)
            
        
    except UserProfile.DoesNotExist:
        print({"detail": "User profile not found for provided ID token."})
        return HttpResponse({"detail": "User profile not found for provided ID token."}, status=404)
    
    except Note.DoesNotExist:
        print("Note not found in database, creating entry now!")
        decoded_token= auth.verify_id_token(id_token)
        uid= decoded_token.get('uid')
        user_profile_instance= UserProfile.objects.get(uid=uid)
        print(note_data)
        
        note_data.pop('old_title', None)
        note_data.pop('old_body', None)
        
        serializer= NoteSerializer(data=note_data)
        if serializer.is_valid():
            serializer.save(user= user_profile_instance)
            return HttpResponse("Note is saved!", status= 201)
        
    except Exception as e:
        print({"detail": f"Error verifying ID token: {str(e)}"})
        return HttpResponse({"detail": f"Error verifying ID token: {str(e)}"}, status=400)
