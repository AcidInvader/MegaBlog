from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Article, Category, Comment

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name']


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=200, allow_unicode=True)

class ArticleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'image', 
                  'created', 'category', 'author']

    


    