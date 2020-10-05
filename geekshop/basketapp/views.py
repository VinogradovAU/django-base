from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    title = "Корзина"
    content = {
        "title": title,
    }
    return render(request, 'basketapp/basket.html', content)


def basket_add(request, pk):
    # получаем объект продукта для добавления в корзину
    product_item = get_object_or_404(Product.objects, id=pk)

    # проверяем, может такой товар уже добвлен в корзину
    basket_item = Basket.objects.filter(user=request.user, product=product_item).first()

    # если None то нет (небыло) такого товара в корзине
    if not basket_item:
        basket_item = Basket.objects.create(user=request.user, product=product_item)  # добавляем новый товар в корзину

    basket_item.quantity += 1  # добавляем колическтво к существующему товару
    basket_item.save()  # делаем коммит в базу

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # возврат пользователя туда где он был


def basket_remove(request, pk):
    # удаляем товар
    basket = Basket.objects.filter(user=request.user, product__id=pk).delete()

    # читаем список товаров пользователя для вывода
    basket = Basket.objects.filter(user=request.user)

    content = {
        "title": "корзина",
        "basket": basket,
        "total_all_price": calc_total_price(basket),

    }
    return render(request, "basketapp/basket.html", content)


def basket_view(request):
    basket = Basket.objects.filter(user=request.user)

    content = {
        "title": "корзина",
        "basket": basket,
        "total_all_price": calc_total_price(basket),
    }

    return render(request, "basketapp/basket.html", content)


def calc_total_price(obj):
    # obj - объект корзины конкретного пользователя
    total_all_price = 0
    for k in obj:
        total_for_item = k.product.price * k.quantity
        total_all_price += total_for_item
    return total_all_price


def count_items(obj):
    # obj - объект корзины конкретного пользователя

    count_items = 0 #переменная для суммы товаров
    for k in obj:
        count_items += k.quantity

    return count_items
