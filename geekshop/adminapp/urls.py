import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('user/create/', adminapp.user_create, name='user_create'),
    path('user/read/', adminapp.users, name='users'), # выводим список пользователей
    path('user/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('user/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('user/recovery/<int:pk>/', adminapp.user_recovery, name='user_recovery'),

    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/read/', adminapp.categories, name='categories'),  # выводим список категорий
    path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('categories/recovery/<int:pk>/', adminapp.category_recovery, name='category_recovery'),

    path('product/create/category/<int:pk>/', adminapp.product_create, name='product_create'), # выводим список продуктов в категории
    path('product/read/category/<int:pk>/', adminapp.products, name='products'),  # выводим один продукт
    path('product/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('product/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),

]
