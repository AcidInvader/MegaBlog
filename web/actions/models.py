from django.db import models
from django.contrib.auth import get_user_model
from blog.models import Article
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class LikeStatus(models.IntegerChoices):
    LIKE = 1
    DISLIKE = 0


def like_content_limit():
    return models.Q(app_label="blog", model="article") | models.Q(app_label="blog", model="comment")

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now=True)
    vote = models.PositiveSmallIntegerField(choices=LikeStatus.choices)
    content_type = models.ForeignKey(ContentType, limit_choices_to=like_content_limit, on_delete=models.CASCADE, related_name="likes")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


