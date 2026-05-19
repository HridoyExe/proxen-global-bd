from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsAdminOrReadOnly

@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="Get a list of all categories. Supports searching by `name`."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Get detailed information about a specific category."))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_description="Create a new category. Only accessible by admins."))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_description="Update an existing category. Only accessible by admins."))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_description="Partially update an existing category. Only accessible by admins."))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_description="Delete a category. Only accessible by admins."))
class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category API Endpoints
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="Get a list of all products.\n- **Pagination**: 10 products per page.\n- **Filtering**: `?category=ID` or `?category__slug=slug`.\n- **Searching**: `?search=name_or_sku`.\n- **Ordering**: `?ordering=price` or `?ordering=-created_at`."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Get detailed information about a specific product."))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_description="Create a new product. Only accessible by admins."))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_description="Update an existing product. Only accessible by admins."))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_description="Partially update an existing product. Only accessible by admins."))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_description="Delete a product. Only accessible by admins."))
class ProductViewSet(viewsets.ModelViewSet):
    """
    Product API Endpoints
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'category__slug']
    ordering_fields = ['price', 'created_at']
    search_fields = ['name', 'description', 'sku']

