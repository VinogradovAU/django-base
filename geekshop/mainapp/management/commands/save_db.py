from django.core.management import BaseCommand
from django.conf import settings
import os
import json
import datetime
import sys
from django.core.management import call_command


FILE_NAME = os.path.join(settings.BASE_DIR + '\mainapp\json')


def decode_file_ascii(filename):
    with open(f'{FILE_NAME}\{filename}', 'r', encoding="utf-8") as fd:
        data_j = json.load(fd)
        # print(data_j)

    with open(f'{FILE_NAME}\{filename}', 'w', encoding="utf-8") as fd:
        json.dump(data_j, fd, ensure_ascii=False, indent=2)


def get_json_data(filename):
    with open(f'{FILE_NAME}\{filename}', 'r', encoding="utf-8") as fd:
        return json.load(fd)


def write_json_data(filename, data_j):
    with open(f'{FILE_NAME}\{filename}', 'w', encoding="utf-8") as fd:
        json.dump(data_j, fd, ensure_ascii=False, indent=2)


class Command(BaseCommand):

    def handle(self, *args, **options):


        # Делаем дамп базы
        dd = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        target_file = f'mainapp_damp_{dd}.json'
        sysout = sys.stdout
        with open(f'{FILE_NAME}\{target_file}', 'w') as fd:
            sys.stdout = fd
            call_command('dumpdata', 'mainapp')
            sys.stdout = sysout

        #Чиним кодировку в созданном дампе
        decode_file_ascii(target_file)


        #Выделяем в отдельные файлы товары, контакты, категории
        # product = []
        # productcategory = []
        # contacts = []
        #
        # data_j = get_json_data(target_file)
        # for k in data_j:
        #     if k['model'] == 'mainapp.product':
        #         product.append(k)
        #         continue
        #     if k['model'] == 'mainapp.productcategory':
        #         productcategory.append(k)
        #     if k['model'] == 'mainapp.contacts':
        #         contacts.append(k)
        # write_json_data('product.json', product)
        # write_json_data('category.json', productcategory)
        # write_json_data('contacts.json', contacts)
