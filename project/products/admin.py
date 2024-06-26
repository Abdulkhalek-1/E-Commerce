from django.contrib import admin

from .models import Product
from .models import ProductImage
from .models import ProductVariation


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = (
        "image",
        "alt_text",
    )
    readonly_fields = ("alt_text",)
    verbose_name = "Product Image"
    verbose_name_plural = "Product Images"


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1
    fields = (
        "variation_name",
        "variation_value",
        "price",
    )
    verbose_name = "Product Variation"
    verbose_name_plural = "Product Variations"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "seller",
        "created_at",
    )
    list_filter = (
        "created_at",
        "seller",
    )
    search_fields = (
        "name",
        "description",
        "seller__email",
    )
    ordering = ("-created_at",)
    inlines = [ProductImageInline, ProductVariationInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "price",
                    "seller",
                ),
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at",),
            },
        ),
    )
    readonly_fields = ("created_at",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "alt_text",
        "image",
    )
    search_fields = (
        "product__name",
        "alt_text",
    )
    ordering = ("product",)


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "variation_name",
        "variation_value",
        "price",
    )
    search_fields = (
        "product__name",
        "variation_name",
        "variation_value",
    )
    ordering = (
        "product",
        "variation_name",
    )
