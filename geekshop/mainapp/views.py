from django.shortcuts import render
import datetime
import random
import os
import json
from mainapp.models import ProductCategory, Product, Contacts
from django.shortcuts import get_object_or_404
from basketapp.models import Basket
from basketapp import views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, DeleteView
from django.conf import settings
from django.core.cache import cache

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

value = datetime.datetime.now()  # значение даты для вывода в копирайт


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user).select_related()
    else:
        return []


def main(request):
    # получаем продукты для вывода на главную
    # products = Product.objects.all()[:4].select_related()
    products = get_products()[:3]

    content = {
        "products": products,
        "title": "Магазин",
        "value": value,  # значение даты для вывода в копирайт
        # "basket": get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', content)


#  перевожу контроллеры на cbv ( с этим - ниже не понятно как рабоатет или нет)
class ProductMainList(ListView):
    model = Product
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        # return Product.objects.filter(is_active=True).select_related()[:4]
        products = get_products()[:4]
        return random.sample(list(products), 1)[0]

    def get_context_data(self, **kwargs):
        context = super(ProductMainList, self).get_context_data(**kwargs)
        context['title'] = 'Магазин'
        context['value'] = value
        # print('ya v kontrollere ProductMainList')
        return context


def product_list(request, pk=None, page=1):
    title = 'продукты'
    links_menu = get_links_menu()
    basket = get_basket(request.user)
    # print('pk:', pk)
    # print('page:', page)

    if pk != None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все',
            }
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related().order_by(
                'price')

        else:

            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True,
                                              category__is_active=True).select_related().order_by('price')

        paginator = Paginator(products, 3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            # 'basket': basket,
        }

        return render(request, 'mainapp/products_list.html', content)


def products(request, pk=None, pk2=None):
    # загружаем названия категорий для формирования меню
    links_menu = get_links_menu()

    if pk != None and pk2 != None:  # прилетели данные на конкретный продукт, его и выводим
        # product_item = get_object_or_404(Product.objects.select_related('category'), id=pk2)
        product_item = get_product(pk2)  # кэширование

        # товары для похожих товаров, та же категория, но кроме показываемого уже
        products_for_sub_menu = Product.objects.filter(category__id=pk, is_active=True). \
                                    exclude(id=pk2).select_related('category')[:3]

        context = {
            "category_num": pk,
            "products_for_sub_menu": products_for_sub_menu,
            "product_item": product_item,
            "value": value,  # значение даты для вывода в копирайт
            "title": "Каталог",
            "links_menu": links_menu,
            # "basket": get_basket(request.user),
        }

        return render(request, 'mainapp/prod.html', context)

    # при переходе на страницу продуктов выводим случайные товары
    if pk == None:
        # products = Product.objects.order_by('?').select_related()[:4]
        products = get_products()[:4]  # кэширование

    else:
        # если указана категория товаров, то выводим товары
        # products = Product.objects.filter(category=pk).select_related().order_by('price')
        products = get_products_in_category_orederd_by_price()  # кэширование

    context = {
        "products": products,
        "value": value,
        "title": "Каталог",
        "links_menu": links_menu,
        # "basket": get_basket(request.user),
    }

    return render(request, 'mainapp/products.html', context)


def contact(request):
    contacts = get_contacts()

    context = {
        "contacts": contacts,
        "title": "Контакты",
        # "basket": get_basket(request.user),
    }

    return render(request, 'mainapp/contact.html', context)


def get_links_menu():
    # return ProductCategory.objects.filter(is_active=True).select_related()

    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)

def get_contacts():
    if settings.LOW_CACHE:
        key = 'contacts'
        contacts = cache.get(key)
        if contacts is None:
            contacts = Contacts.objects.all()
            cache.set(key, contacts)
        return contacts
    else:
        return Contacts.objects.all()


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, \
                                              category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, \
                                      category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, \
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, \
                                      category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, \
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, \
                                      category__is_active=True).order_by('price')
