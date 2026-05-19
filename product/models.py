from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.utils import timezone
from cloudinary.models import CloudinaryField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Category(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    image = CloudinaryField('image', blank=True, null=True)

    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        related_name='variants',
        on_delete=models.CASCADE
    )
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.color or 'N/A'} - {self.size or 'N/A'}"


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )

    variant = models.ForeignKey(
        ProductVariant,
        related_name='variant_images',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    image = CloudinaryField('image')

    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"