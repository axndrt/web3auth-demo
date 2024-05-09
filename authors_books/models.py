import django.db.models
from django.db import models


class Author(models.Model):
    first_name = models.CharField(blank=False, null=False, max_length=30)

    last_name = models.CharField(blank=False, null=False, max_length=30)

    birthday = models.DateTimeField(blank=False, null=False)


class Book(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)

    description = models.TextField(blank=True, null=True, max_length=200)

    author = models.ForeignKey(
        Author, on_delete=django.db.models.PROTECT, related_name="books"
    )

    class Meta:
        unique_together = [["name", "author"], ["name", "description"]]
