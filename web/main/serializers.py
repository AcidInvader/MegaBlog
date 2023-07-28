import pytz
from rest_framework import serializers

from blog.choices import ArticleStatus


class SetTimeZoneSerializer(serializers.Serializer):
    timezone = serializers.ChoiceField(choices=pytz.common_timezones)

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=100)
    last_name = serializers.CharField(min_length=2, max_length=100)
    email = serializers.EmailField()

class Comment(serializers.Serializer):
    author = serializers.EmailField()
    user = UserSerializer()
    content = serializers.CharField(max_length=200)
    # article = ArticleSerializer()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
