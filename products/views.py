from django.conf import settings
from django.views.generic.list import ListView

from products.models import Products, ProductCategory, NewProducts


def view_random_hot_product():
    rand_obj = NewProducts.objects.order_by('?')[0]
    if rand_obj.id:
        view_product = rand_obj.product_key
    else:
        return
    return view_product

# Create your views here.


class IndexView(ListView):
    model = Products
    template_name = 'products/index.html'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = 'Магазин'
        context['icon'] = 'img/icon_add.png'
        context['socials'] = ["social1",
                              "social2",
                              "social3",
                              "social4"]
        context['media_path'] = settings.MEDIA_URL
        return context


class ProductsListView(ListView):
    template_name = 'products/products.html'
    model = Products
    paginate_by = 2

    def get_queryset(self):
        if self.kwargs.get('category_type_id'):
            return Products.objects.filter(category_type_id=self.kwargs.get('category_type_id')).order_by('id')
        else:
            return Products.objects.all().order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог товаров'
        context['icon'] = 'img/icon-hover.png'
        context['controls'] = ["social1",
                               "social2",
                               "social3",
                               "social4"]
        context['media_path'] = settings.MEDIA_URL
        context['categories'] = ProductCategory.objects.all()
        context['hot_product'] = view_random_hot_product()
        if self.kwargs.get('category_type_id'):
            context['category_type_id'] = self.kwargs.get('category_type_id')
        return context








