from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from blog.models import Article, Category, ArticleStatus, Comment
from django.db.models import QuerySet
from . import serializers
from main import pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from api.v1.auth_app import utils


class BlogListView(ListAPIView):
    permission_classes = ()
    serializer_class = serializers.ArticleSerializer
    pagination_class = pagination.BasePageNumberPagination
    
    def get_queryset(self) -> QuerySet[Article]:
        return Article.objects.filter(status=ArticleStatus.ACTIVE)

    '''
    Такую же логику получаем из ListAPIView.ListModelMixin
    '''
    # def get(self, request):
    #     queryset = self.get_queryset()
    #     paginator = self.paginate_queryset(queryset)
    #     serializer = self.get_serializer(paginator, many=True)
    #     return self.get_paginated_response(serializer.data)
    

class BlogDetailView(RetrieveAPIView):
    permission_classes = ()
    serializer_class = serializers.ArticleDetailSerializer

    def get_queryset(self) -> QuerySet[Article]:
        return Article.objects.all()

    # def get(self, request, pk):
    #     print(f'{self.kwargs=}')
    #     article = self.get_object()
    #     serializer = self.get_serializer(article)
    #     print(f"{article=}")
    #     return Response(serializer.data)

class SlugDetailView(RetrieveAPIView):
    permission_classes = ()
    serializer_class = serializers.ArticleDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self) -> QuerySet[Article]:
        return Article.objects.all()
   
    
class ArticleCreateView(CreateAPIView):
    serializer_class = serializers.ArticleCreateSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save()
        article_id = serializer.data['id']
        user = self.request.user
        utils.send_article_admin_mail(article_id)
        utils.send_article_created_mail(user)
    

class CategoryListView(ListAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self) -> QuerySet[Category]:
        return Category.objects.all()
    

class CommentCreateView(CreateAPIView):
    serializer_class = serializers.CommentCreateSerializer


class CommentListView(ListAPIView):
    serializer_class = serializers.CommentListSerializer
    pagination_class = pagination.BasePageNumberPagination

    def get_queryset(self):
        article_id = self.kwargs['article_pk']
        print('kwargs', self.kwargs)
        return Comment.objects.filter(article_id=article_id, parent__isnull=True)
