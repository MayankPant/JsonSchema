from rest_framework import serializers
from .models import User, Schema

class UserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # Customize the format if needed

    class Meta:
        model = User
        fields = ['user_id', 'username', 'user_email', 'profile_picture_url', 'created_at']

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None

class SchemaSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Schema
        fields = '__all__'
