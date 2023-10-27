from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from main.models import User
from django.db.models import QuerySet
from . import serializers
from main import pagination
from rest_framework.permissions import AllowAny


User = get_user_model()

class UserListView(ListAPIView):
    permission_classes = ()
    serializer_class = serializers.UserListSerializer
    pagination_class = pagination.BasePageNumberPagination


    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()
    
class CurentUserView(GenericAPIView):
    serializer_class = serializers.CurentUserSerializer
    
    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)

        return Response(serializer.data)
    

class UpdateUserView(UpdateAPIView):
    serializer_class = serializers.CurentUserSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        print(f"{kwargs=}")
        return super().patch(request, *args, **kwargs)


    




    