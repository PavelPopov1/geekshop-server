from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from basket.models import Basket
from products.models import Products


# Create your views here.

class BasketAddView(LoginRequiredMixin, ListView):
    model = Products
    template_name = 'products/index.html'

    def get(self, request, *args, **kwargs):
        product = Products.objects.get(id=self.kwargs['product_id'])
        basket = Basket.objects.filter(user=request.user,
                                       product=product)
        if not basket:
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            bask = basket.first()
            bask.quantity += 1
            bask.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketDelView(LoginRequiredMixin, ListView):
    model = Products
    template_name = 'products/index.html'

    def get(self, request, *args, **kwargs):
        Basket.objects.get(id=self.kwargs['id']).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# контекстный процессор тут не работает при нажатии на кнопки увеличить-уменьшить
# не очень понял причину
'''class BasketEditView(LoginRequiredMixin, ListView):
    model = Products
    template_name = 'products/index.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            bask = Basket.objects.get(id=self.kwargs['id'])
            if self.kwargs['quantity']:
                bask.quantity = self.kwargs['quantity']
                bask.save()
            else:
                bask.delete()
            # basket = Basket.objects.filter(user=request.user)
            # context = {'basket': basket}
            result = render_to_string('basket/basket.html')
            return JsonResponse({'result': result})
        else:
            return super(BasketEditView, self).get(request, *args, **kwargs)'''


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        # baskets = Basket.objects.filter(user=request.user)
        # context = {'basket': baskets}
        result = render_to_string('basket/basket.html', request=request)
        return JsonResponse({'result': result})



