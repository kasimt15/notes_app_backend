from rest_framework import serializers
from .models.note import Note, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['uid', 'display_name', 'email']

class NoteSerializer(serializers.ModelSerializer):
    user_display = serializers.CharField(source='user.display_name', read_only=True)
     
    class Meta:
        model = Note
        fields = ['id', 'title', 'body','user_display', 'user_display']
        read_only_fields = ['user_display']  
        extra_kwargs = {
            'user': {'write_only': True} # 'user' foreign key should only be written (sent by client)
        }