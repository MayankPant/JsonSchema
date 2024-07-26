from rest_framework import serializers
from .models import User, Schema

class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # Customize the format if needed

    class Meta:
        model = User
        fields = ['user_id', 'username', 'user_email', 'profile_picture', 'file_hash', 'created_at']

    

class SchemaSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Schema
        fields = '__all__'
