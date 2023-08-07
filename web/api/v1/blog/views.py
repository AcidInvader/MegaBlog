from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from blog.models import Article
from django.db.models import QuerySet
from . import serializers
from main import pagination

class BlogListView(ListAPIView):
    permission_classes = ()
    serializer_class = serializers.ArticleSerializer
    pagination_class = pagination.BasePageNumberPagination
    

    def get_queryset(self) -> QuerySet[Article]:
        return Article.objects.all()

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