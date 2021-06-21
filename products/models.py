from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(unique=True, max_length=64)
    description = models.TextField(blank=True)


# Create your models here.
class Products(models.Model):
    name = models.CharField(unique=True, max_length=64)
    description = models.TextField(blank=True)
    product_img = models.ImageField(blank=True, upload_to="products_img")
    price = models.DecimalField(decimal_places=2, max_digits=32)
    category_type = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)


class NewProducts(models.Model):
    product_key = models.ForeignKey(Products, on_delete=models.CASCADE)


