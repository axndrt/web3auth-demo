import django.db.models
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=30)

    last_name = models.CharField(max_length=30)

    birthday = models.DateTimeField()


class Book(models.Model):
    name = models.CharField(max_length=50)

    description = models.TextField(blank=True, max_length=200)

    author = models.ForeignKey(
        Author, on_delete=django.db.models.PROTECT, related_name="books"
    )

    class Meta:
        unique_together = [["name", "author"], ["name", "description"]]
