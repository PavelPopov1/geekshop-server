from django.contrib import admin
from products.models import Products, ProductCategory, Menu

admin.site.register(Products)
admin.site.register(ProductCategory)
admin.site.register(Menu)

# Register your models here.
