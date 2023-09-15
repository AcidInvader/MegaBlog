from typing import TypeVar, Optional

from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

UserType = TypeVar('UserType', bound='User')

def upload_avatar_path(instance: 'User', filename: str) -> str:
    return f"avatars/{instance.id}/{filename}"

class User(AbstractUser):
    class Gender(models.IntegerChoices):
        MALE = (1, "male")
        FEMALE = (2, "female")
        NONE = (0, "undefined")

    username = None  # type: ignore
    email = models.EmailField(_('Email address'), unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_avatar_path, default="avatars/default.png")
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=Gender.choices, default=Gender.NONE)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return super().get_full_name()

    @property
    def confirmation_key(self) -> str:
        return signing.dumps(obj=self.pk)
    
    @classmethod
    def get_user(cls, key: str) -> Optional['User']:
        max_age = 600
        try:
            user_id = signing.loads(key, max_age=max_age)
            user = cls.objects.get(id=user_id)
        except(signing.SignatureExpired, signing.BadSignature, cls.DoesNotExist):
            return None 

        return user

