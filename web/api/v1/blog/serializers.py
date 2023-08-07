from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from blog.models import Article, Comment
from main.models import User


User = get_user_model()
class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'full_name']


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=200, allow_unicode=True)


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'category', 'author', 'image', 'updated']

class ArticleDetailSerializer(ArticleSerializer):

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ['content']



    

    


    