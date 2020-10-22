
import mainapp.views as mainapp
from django.urls import path

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name="index"),
    path('category/<int:pk>/page/<int:page>', mainapp.product_list, name="page"),
    path('category/<int:pk>/', mainapp.products, name="category"),
    path('category/<int:pk>/<int:pk2>/', mainapp.products, name="product"),

]

