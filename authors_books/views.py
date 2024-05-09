from rest_framework import filters, viewsets
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
    JWTTokenUserAuthentication,
)

from authors_books.models import Author, Book
from authors_books.serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = AuthorSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ["first_name", "last_name"]


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    authentication_classes = [JWTTokenUserAuthentication]
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name", "author__first_name", "author__last_name"]

    def get_queryset(self):
        return Book.objects.all().select_related("author")
