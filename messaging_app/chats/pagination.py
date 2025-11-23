from rest_framework.pagination import CursorPagination


class MessagesPagination(CursorPagination):
    page_size = 20
    ordering = "-sent_at"
