from django.db import models
from django.conf import settings
from mainapp.models import Product


# модель корзины товаров
class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    def product_cost(self):
        "возвращает цену одной корзинки (кол-во продуктов * на цену единицы)"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        "возвращает общее количнество всех товаров в корзине"
        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        "возвращает ИОТОГО всей корзины - всех покупок"
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost
