from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForms, ShopUserRegisterForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse
from authapp.models import ShopUser
from django.conf import settings
from django.core.mail import send_mail

def send_verification_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    subject = f'Активация пользователя {user.username}'

    message = f'Для подтверждения пелейдите по ссылке:\n {settings.DOMAIN_NAME}{verify_link}'

    print('send_verification_email->отправляем письмо')
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main'))




def login(request):
    title = "вход"

    login_form = ShopUserLoginForms(data=request.POST or None)
    next = request.GET.get('next', '')

    print('--1--',next)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)  # добавляем объект пользователя в request
            if 'next' in request.POST.keys():
                print('--2--', request.POST)
                return HttpResponseRedirect(request.POST['next'])

            print('--3--', next)
            return HttpResponseRedirect(reverse('main'))

    # если не было запроса POST, то собираем контекст и выводим пользователю страницу входа
    content = {'title': title, 'login_form': login_form, 'next': next}
    print('a тут')
    return render(request, 'authapp/login.html', content)


def logout(request):
    # удаляем объект пользователя из request
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            # register_form.save()
            # return HttpResponseRedirect(reverse('auth:login'))
            user = register_form.save()
            if send_verification_email(user):
                print('success')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('error')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}
    return render(request, 'authapp/register.html', content)

def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {'title': title, 'edit_form': edit_form }

    return render(request, 'authapp/edit.html', content)
