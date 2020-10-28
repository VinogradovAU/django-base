from django.core.management import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from authapp.models import ShopUser

import os
import json

from mainapp.models import Product
from mainapp.models import ProductCategory
from mainapp.models import Contacts

from django.core.management import call_command

FILE_NAME = os.path.join(settings.BASE_DIR + '\mainapp\json')


def get_json_data(filename):
    with open(f'{FILE_NAME}\{filename}', 'r', encoding="utf-8") as fd:
        return json.load(fd)


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Очищаем базу данных
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        Contacts.objects.all().delete()

        # Загружаем базу данных из дампа
        target_file = 'mainapp_damp.json'
        call_command('loaddata', f'{FILE_NAME}\{target_file}')

        super_user = ShopUser.objects.create_superuser(username='django', email='admin@admin.ru', password='geekbrains', age=30)

# Дамп базы данных в файл фикстур
# python manage.py dumpdata --format=json myapp > myapp/fixtures/initial_data.json
#
# По умолчанию фикстуры нужно хранить в папке fixtures, которую нужно создать внутри каждого приложения.
# Если фикстуры сохраняются в файл с названием initial_data, то при каждом syncdb фикстуры будут загружаться
# в базу данных вашего проекта.
#
# Загрузка фикстуры из файла
# python manage.py loaddata myapp/fixtures/myfix.json
