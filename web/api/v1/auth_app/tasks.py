from celery import shared_task
from src import settings
from main.models import UserType
from django.contrib.auth import get_user_model
from .utils import send_verify_mail, SendEmailHandler


User: UserType = get_user_model()

@shared_task
def send_verify_mail_task(user_id: int):
    user = User.objects.get(id=user_id)

    return send_verify_mail(user)


@shared_task
def send_reset_password_mail_task(user, uid, token):
    mail = SendEmailHandler(user, uid, token)

    return mail.send_reset_password_mail()