from rest_framework import routers

from authors_books.views import AuthorViewSet, BookViewSet

router = routers.SimpleRouter()
router.register(r"authors", AuthorViewSet, basename="authors")
router.register(r"books", BookViewSet, basename="books")

urlpatterns = router.urls
