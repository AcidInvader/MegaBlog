from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from blog.models import Article
from django.db.models import QuerySet
from . import serializers
from main.pagination import BasePageNumberPagination


class BlogListView(GenericAPIView):
    permission_classes = ()
    serializer_class = serializers.ArticleListSerializer
    pagination_class = BasePageNumberPagination

    def get_queryset(self) -> QuerySet[Article]:
        return Article.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        # serializer = self.serializer_class(queryset, many=True, context={
        #     "request": request,
        # })
        paginator = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginator, many=True)

        return self.get_paginated_response(serializer.data)