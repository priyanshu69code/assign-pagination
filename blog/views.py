from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticleSerializer
from .models import Article
# Create your views here.


class ArticlePageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = ArticlePageNumberPagination

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)
        try:
            page_num = int(page)
            if page_num < 1:
                return Response({
                    'detail': 'Invalid page number. Page numbers start from 1.',
                    'error': 'invalid_page'
                }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'detail': f'Invalid page number "{page}". Page must be a number.',
                'error': 'invalid_page'
            }, status=status.HTTP_404_NOT_FOUND)
        queryset = self.filter_queryset(self.get_queryset())
        page_obj = self.paginate_queryset(queryset)
        if page_obj is None and page_num > 1:
            paginator = self.pagination_class()
            paginator.page_size = self.pagination_class.page_size
            from django.core.paginator import Paginator
            django_paginator = Paginator(queryset, paginator.page_size)
            return Response({
                'detail': f'Page {page_num} is out of range. Available pages: 1-{django_paginator.num_pages}',
                'error': 'page_out_of_range',
                'total_pages': django_paginator.num_pages
            }, status=status.HTTP_404_NOT_FOUND)

        if page_obj is not None:
            serializer = self.get_serializer(page_obj, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
