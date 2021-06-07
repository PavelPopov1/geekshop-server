from django.shortcuts import render
from products.models import Products, ProductCategory, Menu
from django.conf import settings



# Create your views here.
def index(request):
    products_list = Products.objects.all()
    context = {
        "title": "Магазин",
        "products": products_list,
        "icon": "img/icon-hover.png",
        "socials": ["social1",
                    "social2",
                    "social3",
                    "social4"],
        "media_path": settings.MEDIA_URL
    }
    return render(request, 'products/index.html', context)


def products(request):
    products_list = Products.objects.all()
    menu = Menu.objects.all()
    context = {
        "title": "Каталог товаров",
        "menus": menu,
        "products": products_list,
        "icon": "img/icon-hover.png",
        "controls": [
            "img/controll.jpg",
            "img/controll1.jpg",
            "img/controll2.jpg"
        ],
        "socials": ["social1",
                    "social2",
                    "social3",
                    "social4"],
        "media_path": settings.MEDIA_URL
    }
    return render(request, 'products/products.html', context)

