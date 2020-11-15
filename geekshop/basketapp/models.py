from django.db import models
from django.conf import settings
from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super(BasketQuerySet, self).delete(*args, **kwargs)


# модель корзины товаров
class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    @property
    def product_cost(self):
        "возвращает цену одной корзинки (кол-во продуктов * на цену единицы)"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        "возвращает общее количнество всех товаров в корзине"
        # _items = Basket.objects.filter(user=self.user).exclude(is_active=False).select_related()
        _items = Basket.objects.filter(user=self.user, is_active=True).select_related()
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        "возвращает ИОТОГО всей корзины - всех покупок"
        # _items = Basket.objects.filter(user=self.user).exclude(is_active=False).select_related()
        _items = Basket.objects.filter(user=self.user).exclude(is_active=False).select_related()
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    @staticmethod
    def get_items(user):
        result = Basket.objects.filter(user=user).select_related('product').order_by('product__category')
        return result

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_item(self.pk)
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(Basket, self).save(*args, **kwargs)
