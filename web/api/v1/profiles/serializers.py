from rest_framework.serializers import Serializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from main.models import User

class UserListSerializer(serializers.ModelSerializer):
    
    class  Meta:
        model = User
        fields = ['id', 'full_name', 'email']