from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product
from mainapp import views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def basket(request):
    title = "Корзина"
    content = {
        "title": title,
    }
    return render(request, 'basketapp/basket.html', content)

@login_required
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

@login_required
def basket_remove(request, pk):
    # удаляем товар
    basket = Basket.objects.filter(user=request.user, product__id=pk).delete()

    basket = Basket.objects.filter(user=request.user)
    content = {
        "title": "корзина",
        "basket": basket,
    }
    return render(request, "basketapp/basket.html", content)

@login_required
def basket_view(request):

    basket = Basket.objects.filter(user=request.user)
    # calc_total_price = calc_total_price(basket)

    content = {
        "title": "корзина",
        "basket": basket,
    }

    return render(request, "basketapp/basket.html", content)


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user). \
            order_by('product__category')

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', \
                                  content)

        return JsonResponse({'result': result})

# def calc_total_price(obj):
#     # obj - объект корзины конкретного пользователя
#     total_all_price = 0
#     for k in obj:
#         total_for_item = k.product.price * k.quantity
#         total_all_price += total_for_item
#     return total_all_price
#
#
# def count_items(obj):
#     # obj - объект корзины конкретного пользователя
#
#     count_items = 0  # переменная для суммы товаров
#     for k in obj:
#         count_items += k.quantity
#
#     return count_items
