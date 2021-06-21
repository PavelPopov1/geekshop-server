from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class BasketEditView(LoginRequiredMixin, ListView):
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
            basket = Basket.objects.filter(user=request.user)
            context = {'basket': basket}
            result = render_to_string('basket/basket.html', context)
            return JsonResponse({'result': result})
        else:
            return super(BasketEditView, self).get(request, *args, **kwargs)



