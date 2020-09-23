from django.shortcuts import render
import datetime
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


try:

    with open(f'{BASE_DIR}\db_test.json', 'r', encoding="utf-8") as fd:

        data = json.load(fd)
        print(data)
        db_content = data['db_content']
        links_menu = data['links_menu']

except Exception:
    db_content = ''
    links_menu = [{'href':'products_all', 'name':'все'},]


# Create your views here.
# db_content = [
#     {"prod_name":"TV System", "price": 200,},
#     {"prod_name":"SoundSystem", "price": 300,},
#     {"prod_name":"GSM Antenna", "price": 400,},
# ]

value = datetime.datetime.now() # значение даты для вывода в копирайт

# links_menu = [
#     {'href':'products_all', 'name':'все'},
#     {'href':'products_home', 'name':'дом'},
#     {'href':'products_office', 'name':'офис'},
#     {'href':'products_modern', 'name':'модерн'},
#     {'href':'products_classic', 'name':'классика'},
# ]

def main(request):
    content = {
        "test": "123 Andry",
        "db_content": db_content,
        "user": request.user,
        "value": value,
        "title": "Магазин",
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    context = {
        "value": value,
        "title": "Каталог",
        "links_menu": links_menu,
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    context = {
        "value": value,
        "title": "Контакты",
    }
    return render(request, 'mainapp/contact.html', context)
