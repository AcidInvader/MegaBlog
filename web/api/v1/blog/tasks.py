from celery import shared_task
from src import settings
from .utils import send_article_admin_mail, send_article_created_mail
from main.models import UserType
from django.contrib.auth import get_user_model

User: UserType = get_user_model()

@shared_task
def send_article_admin_mail_task(article_id: int):

    return send_article_admin_mail(article_id)


@shared_task
def send_article_created_mail_task(user_id: int):
    user = User.objects.get(id=user_id)

    return send_article_created_mail(user)