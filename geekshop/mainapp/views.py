from django.shortcuts import render
import datetime
import os
import json
from .models import ProductCategory, Product, Contacts

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# try:
#
#     with open(f'{BASE_DIR}\db_test.json', 'r', encoding="utf-8") as fd:
#
#         data = json.load(fd)
#         print(data)
#         db_content = data['db_content']
#         links_menu = data['links_menu']
#
# except Exception:
#     db_content = ''
#     links_menu = [{'href':'products_all', 'name':'все'},]


# Create your views here.


value = datetime.datetime.now() # значение даты для вывода в копирайт


def main(request):

    products = Product.objects.all()[:4]

    content = {
        "products": products,
        "title": "Магазин",
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):

    links_menu = ProductCategory.objects.all()

    #при переходе на страницу продуктов открываем продукты первой категории
    if pk == None:
        products = Product.objects.filter(category=links_menu[0])
    else:
        products = Product.objects.filter(category=pk)

    context = {
        "products": products,
        "value": value,
        "title": "Каталог",
        "links_menu": links_menu,
    }

    return render(request, 'mainapp/products.html', context)


def contact(request):
    contacts = Contacts.objects.all()[:3]
    context = {
        "contacts": contacts,
        "title": "Контакты",
    }

    return render(request, 'mainapp/contact.html', context)
