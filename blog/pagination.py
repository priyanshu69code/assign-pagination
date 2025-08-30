from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError


class CustomArticlePagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                page_size = int(request.query_params[self.page_size_query_param])
                if page_size <= 0:
                    raise ValueError("Page size must be positive")
                if page_size > self.max_page_size:
                    raise ValueError(f"Page size cannot exceed {self.max_page_size}")
                return page_size
            except (KeyError, ValueError) as e:
                if isinstance(e, ValueError):
                    self.page_size_error = str(e)
                pass
        return self.page_size

    def get_paginated_response(self, data):
        if hasattr(self, 'page_size_error'):
            return Response({
                'error': 'Invalid page_size parameter',
                'detail': self.page_size_error,
                'valid_range': f'1 to {self.max_page_size}'
            }, status=status.HTTP_400_BAD_REQUEST)
        total_items = self.page.paginator.count
        current_page = self.page.number
        total_pages = self.page.paginator.num_pages
        page_size = len(data)
        has_next = self.page.has_next()
        has_previous = self.page.has_previous()
        start_item = (current_page - 1) * self.get_page_size(self.request) + 1
        end_item = start_item + page_size - 1

        return Response({
            'page_info': {
                'current_page': current_page,
                'total_pages': total_pages,
                'has_next': has_next,
                'has_previous': has_previous,
                'next_page': current_page + 1 if has_next else None,
                'previous_page': current_page - 1 if has_previous else None,
            },
            'items_info': {
                'count_on_page': page_size,
                'total_items': total_items,
                'page_size': self.get_page_size(self.request),
                'item_range': {
                    'start': start_item,
                    'end': end_item
                }
            },
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'results': data
        })

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        page_size = self.get_page_size(request)
        if hasattr(self, 'page_size_error'):
            return []

        return super().paginate_queryset(queryset, request, view)
