
import mainapp.views as mainapp
from django.urls import path

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name="index"),
    path('<int:pk>/', mainapp.products, name="category"),
    path('<int:pk>/<int:pk2>/', mainapp.products, name="product"),
]

