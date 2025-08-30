from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticleSerializer
from .models import Article
from .pagination import CustomArticlePagination
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)

        try:
            page_num = int(page)
            if page_num < 1:
                return Response({
                    'error': 'Invalid page number',
                    'detail': 'Page numbers must be positive integers starting from 1.',
                    'provided_page': page
                }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'error': 'Invalid page number',
                'detail': f'Page must be a valid integer. Received: "{page}"',
                'provided_page': page
            }, status=status.HTTP_404_NOT_FOUND)

        # Get queryset and paginate
        queryset = self.filter_queryset(self.get_queryset())

        # Check for page_size validation errors first
        paginator = self.pagination_class()
        page_size = paginator.get_page_size(request)
        if hasattr(paginator, 'page_size_error'):
            return Response({
                'error': 'Invalid page_size parameter',
                'detail': paginator.page_size_error,
                'valid_range': f'1 to {paginator.max_page_size}'
            }, status=status.HTTP_400_BAD_REQUEST)

        page_obj = self.paginate_queryset(queryset)

        # Handle page out of range
        if page_obj is None and page_num > 1:
            from django.core.paginator import Paginator
            django_paginator = Paginator(queryset, page_size)
            return Response({
                'error': 'Page out of range',
                'detail': f'Page {page_num} does not exist.',
                'total_pages': django_paginator.num_pages,
                'provided_page': page_num,
                'valid_range': f'1 to {django_paginator.num_pages}'
            }, status=status.HTTP_404_NOT_FOUND)

        if page_obj is not None:
            serializer = self.get_serializer(page_obj, many=True)
            return self.get_paginated_response(serializer.data)

        # Fallback for edge cases
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ArticleListCustomBenchmarkView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = CustomArticlePagination

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('-created_at')


    def list(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)

        try:
            page_num = int(page)
            if page_num < 1:
                return Response({
                    'error': 'Invalid page number',
                    'detail': 'Page numbers must be positive integers starting from 1.',
                    'provided_page': page
                }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'error': 'Invalid page number',
                'detail': f'Page must be a valid integer. Received: "{page}"',
                'provided_page': page
            }, status=status.HTTP_404_NOT_FOUND)

        # Get queryset and paginate
        queryset = self.filter_queryset(self.get_queryset())

        # Check for page_size validation errors first
        paginator = self.pagination_class()
        page_size = paginator.get_page_size(request)
        if hasattr(paginator, 'page_size_error'):
            return Response({
                'error': 'Invalid page_size parameter',
                'detail': paginator.page_size_error,
                'valid_range': f'1 to {paginator.max_page_size}'
            }, status=status.HTTP_400_BAD_REQUEST)

        page_obj = self.paginate_queryset(queryset)

        # Handle page out of range
        if page_obj is None and page_num > 1:
            from django.core.paginator import Paginator
            django_paginator = Paginator(queryset, page_size)
            return Response({
                'error': 'Page out of range',
                'detail': f'Page {page_num} does not exist.',
                'total_pages': django_paginator.num_pages,
                'provided_page': page_num,
                'valid_range': f'1 to {django_paginator.num_pages}'
            }, status=status.HTTP_404_NOT_FOUND)

        if page_obj is not None:
            serializer = self.get_serializer(page_obj, many=True)
            return self.get_paginated_response(serializer.data)

        # Fallback for edge cases
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
