from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.conf import settings
from django.core.management import call_command


class TestUserTestCase(TestCase):
    USERNAME = 'tarantino'
    PASS = 'geekbrains'
    expected_success_code = 200
    expected_redirect_code = 302

    def setUp(self):
        # call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')

        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser('django2', 'django2@geekshop.local', 'geekbrains')

        self.user = ShopUser.objects.create_user('tarantino', 'tarantino@geekshop.local', 'geekbrains')

        self.user_with__first_name = ShopUser.objects.create_user('umaturman', \
                                                                  'umaturman@geekshop.local', 'geekbrains',
                                                                  first_name='Ума')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Магазин')
        self.assertNotContains(response, 'Пользователь', status_code=self.expected_success_code)

        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username=self.USERNAME, password=self.PASS)

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=self.expected_success_code)
        self.assertEqual(response.context['user'], self.user)

        # выходим из системы
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, self.expected_redirect_code)

    # def tearDown(self):
    # call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')

    # проверяем переадресацию при доступе к корзине
    def test_basket_login_redirect(self):
        # без логина - переадресация
        response = self.client.get('/basket/view')
        self.assertEqual(response.url, '/auth/login/?next=/basket/view')
        self.assertEqual(response.status_code, self.expected_redirect_code)

        # с логином все ok
        self.client.login(username='tarantino', password='geekbrains')

        response = self.client.get('/basket/view')
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/view')
        self.assertIn('Shopping Cart', response.content.decode())

    # проверяем выход из системы
    def test_user_logout(self):
        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertFalse(response.context['user'].is_anonymous)

        # выходим из системы
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, self.expected_redirect_code)

        # главная после выхода
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertTrue(response.context['user'].is_anonymous)

    #
    # тест регистрации пользователя
    def test_user_register(self):
        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@geekshop.local',
            'age': '21'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, self.expected_redirect_code)

        new_user = ShopUser.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.expected_redirect_code)

        # данные нового пользователя
        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertFalse(response.context['user'].is_anonymous)

        # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'], status_code=self.expected_success_code)

    # проверяем не верную регистрацию
    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Мэри',
            'last_name': 'Поппинс',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'merypoppins@geekshop.local',
            'age': '17'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, self.expected_success_code)
        self.assertFormError(response, 'register_form', 'age', 'Вы слишком молоды!')
