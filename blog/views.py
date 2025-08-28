from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .serializers import ArticleSerializer
from .models import Article
# Create your views here.


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 50


    def get_queryset(self):
        return Article.objects.all().order_by('-created_at')
