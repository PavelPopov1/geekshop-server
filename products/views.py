from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        "title": "Магазин",
        "products": [
            {"name": "Отличный стул",
             "par": "Расположитесь комфортно.",
             "img": "img/product-1.jpg"},
            {"name": "Стул повышенного качества",
             "par": "Не оторваться.",
             "img": "img/product-2.jpg"}
        ],
        "icon": "img/icon-hover.png",
        "socials": ["social1",
                    "social2",
                    "social3",
                    "social4"]
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        "title": "Каталог товаров",
        "menus": [
            {"name": "все", "href": "#"},
            {"name": "дом", "href": "#"},
            {"name": "офис", "href": "#"},
            {"name": "модерн", "href": "#"},
            {"name": "классика", "href": "#"}
        ],
        "products": [
            {"name": "Стул повышенного качества",
             "par": "Не оторваться.",
             "img": "img/product-11.jpg",
             "href": "#"},
            {"name": "Стул повышенного качества",
             "par": "Не оторваться.",
             "img": "img/product-21.jpg",
             "href": "#"},
            {"name": "Стул повышенного качества",
             "par": "Не оторваться.",
             "img": "img/product-31.jpg",
             "href": "#"}
        ],
        "icon": "img/icon-hover.png",
        "controls": [
            "img/controll.jpg",
            "img/controll1.jpg",
            "img/controll2.jpg"
        ],
        "socials": ["social1",
                    "social2",
                    "social3",
                    "social4"]
    }
    return render(request, 'products/products.html', context)
