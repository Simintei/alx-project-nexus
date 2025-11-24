from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet, AuthorViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'authors', AuthorViewSet)

urlpatterns = router.urls
