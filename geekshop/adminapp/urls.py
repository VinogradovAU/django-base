import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('user/create/', adminapp.user_create, name='user_create'),
    path('user/read/', adminapp.UserListView.as_view(), name='users'), # выводим список пользователей
    path('user/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('user/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('user/user_delete_permanently/<int:pk>/', adminapp.user_delete_permanently, name='user_delete_permanently'),
    path('user/recovery/<int:pk>/', adminapp.user_recovery, name='user_recovery'),

    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.CategoryListView.as_view(), name='categories'),  # выводим список категорий
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.ProductCategoryDeteleView.as_view(), name='category_delete'),
    path('categories/recovery/<int:pk>/', adminapp.ProductCategoryRecoveryView.as_view(), name='category_recovery'),

    path('product/create/category/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'), # выводим список продуктов в категории
    path('product/read/category/<int:pk>/', adminapp.ProductListView.as_view(), name='products'),  # выводим один продукт
    path('product/read/category/<int:pk2>/<int:pk>', adminapp.ProductView.as_view(), name='prod'),  # выводим один продукт
    path('product/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),
    path('product/recovery/<int:pk>/', adminapp.ProductRecoveryView.as_view(), name='product_recovery'),
    # path('product/read/category/<int:pk>/', adminapp.products, name='products'),  # выводим один продукт
    # path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    # path('categories/recovery/<int:pk>/', adminapp.category_recovery, name='category_recovery'),
]
