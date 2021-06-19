from django.contrib import admin
from products.models import Products, ProductCategory, Menu

admin.site.register(ProductCategory)
admin.site.register(Menu)

# Register your models here.


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',
                    'price', 'category_type')
    ordering = ('-price',)
    search_fields = ('name',)