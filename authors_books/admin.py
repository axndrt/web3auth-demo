from django.contrib import admin
from django.db.models import F

from authors_books.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "birthday",
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "author_last_name",
    )

    def author_last_name(self, obj):
        return obj.author_last_name

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(author_last_name=F("author__last_name"))
        )
