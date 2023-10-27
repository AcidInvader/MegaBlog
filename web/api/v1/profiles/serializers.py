from rest_framework.serializers import Serializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from main.models import User
from django.db.models import Count


class UserListSerializer(serializers.ModelSerializer):
    
    class  Meta:
        model = User
        fields = ['id', 'full_name', 'email']


class CurentUserSerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()
    # comment_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "full_name","email", "avatar", "article_count"]
    
    def get_article_count(self, obj: User) -> int:
        queryset = User.objects.filter(id=obj.id)
        queryset = queryset.annotate(article_count=Count("author_of_article"))

        return queryset[0].article_count
    
    # def get_comment_count(self, obj):
    #     queryset = User.objects.filter(id=obj.id)
    #     queryset = queryset.annotate(comment_count=Count("comment_set"))

    #     return queryset[0].comment_count

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        
        return instance
    