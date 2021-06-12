from django.shortcuts import HttpResponseRedirect
from basket.models import Basket
from products.models import Products
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse


# Create your views here.

@login_required
def basket_add(request, product_id):
    product = Products.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user,
                                   product=product)
    if not basket:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        bask = basket.first()
        bask.quantity += 1
        bask.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_del(request, id):
    Basket.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        bask = Basket.objects.get(id=id)
        if bask.quantity:
            bask.quantity = quantity
            bask.save()
        else:
            bask.delete()
        basket = Basket.objects.filter(user=request.user)
        context = {'basket': basket}
        result = render_to_string('basket/basket.html', context)
        return JsonResponse({'result': result})


