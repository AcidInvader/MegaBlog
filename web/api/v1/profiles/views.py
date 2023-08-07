from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from main.models import User
from django.db.models import QuerySet
from . import serializers
from main import pagination


User = get_user_model()

class UserListView(ListAPIView):
    permission_classes = ()
    serializer_class = serializers.UserListSerializer
    pagination_class = pagination.BasePageNumberPagination


    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()

    