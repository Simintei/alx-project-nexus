from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Category, Author
from .serializers import BookSerializer, CategorySerializer, AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed, created, updated, or deleted.
    Pagination is applied automatically through DRF settings.
    """
    queryset = Book.objects.select_related('author', 'category').all()
    serializer_class = BookSerializer

    # Optional enhancements (recommended)
    filter_backends = [DjangoFilterBackend]

    # Filtering examples
    filterset_fields = ["category", "author"]

    # Search examples
    search_fields = ["title", "author"]

    # Sorting examples
    ordering_fields = ["price"]

    def get_schema_fields(self, view):
        return[]
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
