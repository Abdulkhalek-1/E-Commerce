from django.db import models

from project.users.models import Seller


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{super().__str__()}-img-{self.pk}"


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    variation_name = models.CharField(max_length=255)
    variation_value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{super().__str__()}-{self.variation_name}"

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.price
        super().save(*args, **kwargs)
