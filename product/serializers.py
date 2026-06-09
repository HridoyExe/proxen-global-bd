from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_thumbnail(self, obj):
        prefetched = getattr(obj, 'prefetched_products_with_image', None)
        if prefetched is not None:
            first = prefetched[0] if prefetched else None
        else:
            first = obj.products.filter(image__isnull=False).first()
        if first and first.image:
            return first.image.url
        return None

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductVariantSerializer(serializers.ModelSerializer):
    variant_images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None}
