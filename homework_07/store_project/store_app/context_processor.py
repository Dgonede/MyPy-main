from django.db.models import Sum
from .models import OrderProduct

def cart_item_count(request):
    if request.user.is_authenticated:
        # Получаем количество товаров в корзине для аутентифицированного пользователя
        cart_item_count = OrderProduct.objects.filter(order__user=request.user).aggregate(Sum('quantity'))['quantity__sum']
        # Если нет товаров, устанавливаем счетчик в 0
        cart_item_count = cart_item_count if cart_item_count is not None else 0
    else:
        # Если пользователь не аутентифицирован, корзина пуста
        cart_item_count = 0
    return {'cart_item_count': cart_item_count}