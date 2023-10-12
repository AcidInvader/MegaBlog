from main.models import UserType
from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_verify_mail(user: UserType):
    subject = "Verify mail"
    sender = "hello@localhost"
    recipe = [user.email]
    context = {
        "activate_url": get_activate_url(user),
        "full_name": user.full_name,
    }
    html_template = loader.render_to_string("email/sign-up.html", context)
    send_mail(subject, strip_tags(html_template), sender, recipe, html_message=html_template)

def get_activate_url(user: UserType):
    return f"http://127.0.0.1:8888/sign-up/verify?key={user.confirmation_key}"

'''This method send email for reset password'''
def send_reset_password_mail(user: UserType, uid, token):
    subject = "Reset password mail"
    sender = "hello@localhost"
    recipe = [user.email]
    context = {
        'reset_password_url': f"http://127.0.0.1:8888/password-recovery/?uid={uid}&token={token}",
        'full_name': user.first_name,
    }
    html_template = loader.render_to_string('email/reset-password.html', context)
    send_mail(subject, "", sender, recipe, html_message=html_template)


class SendEmailHandler:
    def __init__(self, user, uid: str, token: str):
        self.user = user
        self.uid = uid
        self.token = token

    def send_reset_password_mail(self):
        subject = "Reset password mail"
        sender = "hello@localhost"
        recipe = [self.user.email]
        context = {
        'reset_password_url': f"http://127.0.0.1:8888/password-recovery/?uid={self.uid}&token={self.token}",
        'full_name': self.user.first_name,
        }
        html_template = loader.render_to_string('email/reset-password.html', context)
        send_mail(subject, "", sender, recipe, html_message=html_template)