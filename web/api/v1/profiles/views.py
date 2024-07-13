from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from main.models import User
from django.db.models import QuerySet
from . import serializers
from main import pagination
from rest_framework.permissions import AllowAny
from django.db.models import Count


User = get_user_model()

class UserListView(ListAPIView):
    permission_classes = ()
    serializer_class = serializers.UserListSerializer
    pagination_class = pagination.BasePageNumberPagination


    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()
    
class CurrentUserView(GenericAPIView):
    serializer_class = serializers.CurrentUserSerializer

    def get_object(self):
        return User.objects.annotate(article_count=Count("author_of_article")).get(id=self.request.user.id)
    
    def get(self, request):
        serializer = self.get_serializer(self.get_object())

        return Response(serializer.data)
    

    

class UpdateUserView(UpdateAPIView):
    serializer_class = serializers.CurrentUserSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        print(f"{kwargs=}")
        return super().patch(request, *args, **kwargs)


    




    