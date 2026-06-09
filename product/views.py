import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import filters
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from .models import Category, Product, ProductImage, ProductVariant
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
    queryset = Category.objects.prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(image__isnull=False),
            to_attr='prefetched_products_with_image'
        )
    )
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="Get a list of all products.\n- **Pagination**: 10 products per page.\n- **Filtering**: `?category=ID` or `?category__slug=slug`.\n- **Searching**: `?search=name_or_sku`.\n- **Ordering**: `?ordering=price` or `?ordering=-created_at`."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Get detailed information about a specific product."))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_description="Create a new product with variants and multiple images."))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_description="Update an existing product with variants and multiple images."))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_description="Partially update an existing product."))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_description="Delete a product."))
class ProductViewSet(viewsets.ModelViewSet):
    """
    Product API Endpoints
    """
    queryset = Product.objects.select_related('category').prefetch_related(
        'images',
        'variants',
        'variants__variant_images'
    )
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'category__slug']
    ordering_fields = ['price', 'created_at']
    search_fields = ['name', 'description', 'sku']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        product = serializer.instance
        self._save_extras(request, product)
        
        # Re-fetch product with select_related/prefetch_related to avoid stale cache or N+1 queries in response
        product = self.get_queryset().get(pk=product.pk)
        
        headers = self.get_success_headers(serializer.data)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        product = serializer.instance
        self._save_extras(request, product, is_update=True)
        
        # Re-fetch product with select_related/prefetch_related to avoid stale cache or N+1 queries in response
        product = self.get_queryset().get(pk=product.pk)
        
        return Response(ProductSerializer(product).data)

    def _save_extras(self, request, product, is_update=False):
        # Handle multiple images
        images = request.FILES.getlist('uploaded_images')
        for img in images:
            ProductImage.objects.create(product=product, image=img)
        
        # Handle variants
        variants_data = request.data.get('variants_data')
        if variants_data:
            try:
                variants = json.loads(variants_data)
                if is_update:
                    product.variants.all().delete() 
                
                for v in variants:
                    ProductVariant.objects.create(
                        product=product,
                        color=v.get('color', ''),
                        size=v.get('size', ''),
                        stock=int(v.get('stock', 0))
                    )
            except Exception as e:
                pass 
