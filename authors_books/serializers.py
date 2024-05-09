from rest_framework import serializers

from authors_books.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = (
            "first_name",
            "last_name",
            "birthday",
        )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "name",
            "description",
            "author",
        )
