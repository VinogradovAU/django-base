from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse
from django.conf import settings
import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile

import os


def get_locale(backend, strategy, details, response, user=None, *args, **kwargs):
    if backend.name == 'google-oauth2':
        locale = response["locale"]
        if locale:
            user.shopuserprofile.locale = locale
            user.save()
        # api_url = f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={response["access_token"]}'
        # api_url = f'https://www.googleapis.com/oauth2/v1/profile?access_token={response["access_token"]}'
        # api_url = f'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token={response["access_token"]}'
        # api_url = f'https://www.googleapis.com/oauth2/v1/people/{response["sub"]}&personFields=genders,birthdays'
        api_url = f'https://people.googleapis.com/v1/people/{response["sub"]}&personFields=genders,birthdays'
        # api_url = f'https://people.googleapis.com/v1/people/{response["sub"]}'
        # api_url = f'https://www.googleapis.com/plus/v1/people/{response["sub"]}'
        # api_url = f'https://people.googleapis.com/v1/people/{response["sub"]}?personFields=names,emailAddresses'
        # api_url = f'https://people.googleapis.com/v1/resourceName=people/{response["sub"]}?personFields=names,emailAddresses'

        print('*'*50)
        resp = requests.get(api_url)
        if resp.status_code != 200:
            print("ошибка запроса")
            print('resp:', resp)
            return
        print('resp.status_code:', resp.status_code)
        data = resp.text
        print('data:', data)
        print('*' * 50)

        api_url = f'https://profiles.google.com/{response["sub"]}'
        user.shopuserprofile.profile = api_url
        user.save()


def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    url = None
    BASE_DIR = str(settings.BASE_DIR).replace('\geekshop', '')
    MEDIA_URL = str(settings.MEDIA_URL).replace('/', '\\')
    print('BASE_DIR:', BASE_DIR)

    if backend.name == 'google-oauth2':
        # url = response['image'].get('url')
        url = response["picture"]
        for key in response:
            print(key, '->', response[key])

    if url:
        p = requests.get(url)
        file_name = str(user.email).split('@')[0]
        user_dir = f'{BASE_DIR}{MEDIA_URL}users_avatars'
        user_path_image = f'{user_dir}\{file_name}.jpeg'

        if os.path.isdir(user_dir):
            with open(user_path_image, "wb") as fd:
                fd.write(p.content)
                fd.close()
            user.avatar = user_path_image
            user.save()
            print('user.avatar', user.avatar)
        else:
            print(user_dir, '!!!!!!!!!!NOT DIR!!!!!!!!!!!!')



def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()
