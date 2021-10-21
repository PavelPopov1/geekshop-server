from basket.models import Basket


def baskets(request):
    baskets_list= []
    if request.user.is_authenticated:
        baskets_list = Basket.objects.filter(user = request.user)

    return  {
        'basket' : baskets_list
    }