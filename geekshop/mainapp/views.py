from django.shortcuts import render
import datetime
import random
import os
import json
from .models import ProductCategory, Product, Contacts
from django.shortcuts import get_object_or_404
from basketapp.models import Basket
from basketapp import views


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


value = datetime.datetime.now()  # значение даты для вывода в копирайт

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def main(request):
    #получаем продукты для вывода на главную
    products = Product.objects.all()[:4]

    content = {
        "products": products,
        "title": "Магазин",
        "value": value,  # значение даты для вывода в копирайт
        "basket": get_basket(request.user),
   }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None, pk2=None):

    #загружаем названия категорий для формирования меню
    links_menu = ProductCategory.objects.all().exclude(is_active=False)

    if pk != None and pk2 != None:         # прилетели данные на конкретный продукт, его и выводим
        product_item = get_object_or_404(Product.objects, id=pk2)

        # товары для похожих товаров, та же категория, но кроме показываемого уже
        products_for_sub_menu = Product.objects.filter(category__id=pk).exclude(id=pk2)[:3]

        context = {
            "category_num": pk,
            "products_for_sub_menu": products_for_sub_menu,
            "product_item": product_item,
            "value": value, # значение даты для вывода в копирайт
            "title": "Каталог",
            "links_menu": links_menu,
            "basket": get_basket(request.user),
        }

        return render(request, 'mainapp/prod.html', context)

    # при переходе на страницу продуктов выводим случайные товары
    if pk == None:
        products = Product.objects.order_by('?')[:4]

    else:
        # если указана категория товаров, то выводим товары
        products = Product.objects.filter(category=pk).order_by('price')



    context = {
        "products": products,
        "value": value,
        "title": "Каталог",
        "links_menu": links_menu,
        "basket": get_basket(request.user),
    }

    return render(request, 'mainapp/products.html', context)


def contact(request):
    contacts = Contacts.objects.all()[:3]
    context = {
        "contacts": contacts,
        "title": "Контакты",
        "basket": get_basket(request.user),
    }

    return render(request, 'mainapp/contact.html', context)
