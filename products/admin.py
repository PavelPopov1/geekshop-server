from django.contrib import admin
from products.models import Products, ProductCategory, NewProducts

admin.site.register(ProductCategory)
admin.site.register(NewProducts)

# Register your models here.


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',
                    'price', 'category_type')
    ordering = ('-price',)
    search_fields = ('name',)