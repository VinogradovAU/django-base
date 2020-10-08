from django.urls import path
import basketapp.views as basketapp


app_name = "basketapp"

# CRUD operations for bascet

urlpatterns = [
    path('', basketapp.basket, name="basket"),
    path('add/<int:pk>/', basketapp.basket_add, name="add"),
    path('remove/<int:pk>/', basketapp.basket_remove, name="remove"),
    path('view', basketapp.basket_view, name="view"),
    path('edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name='edit')
]
