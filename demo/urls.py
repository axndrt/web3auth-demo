from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("demo/", include("authors_books.urls")),
    path("auth/", include("web3_auth.urls")),
]
