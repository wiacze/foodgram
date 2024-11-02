from rest_framework.pagination import PageNumberPagination

from foodgram_backend.constants import PAGE_SIZE


class PageLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = PAGE_SIZE
