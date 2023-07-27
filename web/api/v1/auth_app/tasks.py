from celery import shared_task
from .utils import send_verify_mail

@shared_task
def send_verify_mail(user):
    return send_verify_mail(user)