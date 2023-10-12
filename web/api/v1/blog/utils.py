from django.core.mail import send_mail
from django.template import loader
from main.models import UserType


def send_article_admin_mail(article_id):
    subject = "New article just created"
    sender = "hello@localhost"
    recipe = ['neo@local.com']
    context = {
        'article_url': f"http://127.0.0.1:8888/admin/blog/article/{article_id}/change/",
        'full_name': 'Neo',
    }
    html_template = loader.render_to_string('email/article-created-admin.html', context)
    send_mail(subject, "", sender, recipe, html_message=html_template)

def send_article_created_mail(user: UserType):
    subject = "New article just created"
    sender = "hello@localhost"
    recipe = [user.email]
    context = {
        'article_url': f"http://127.0.0.1:8888/",
        'full_name': user.full_name,
    }
    html_template = loader.render_to_string('email/article-created-user.html', context)
    send_mail(subject, "", sender, recipe, html_message=html_template)