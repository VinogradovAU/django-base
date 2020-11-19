from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.db import transaction
from mainapp import views

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm
from mainapp.models import Product
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True).select_related()

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:

            basket_items = Basket.get_items(user=self.request.user).select_related()

            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                    form.initial['item_id'] = basket_items[num].product.pk
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)

        # ----------
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:

            print('Обработка POST формы')
            myformset = OrderFormSet(self.request.POST or None, instance=self.object)
            data['orderitems'] = myformset

            # проверка количестки товара в форме и количества на складе (в базе)
            # проверка идет в forms.py---> clean() - результат в errors
            if not myformset.is_valid():
                print('есть ошибка!!!!!!!!!!')
                # print('non_field_error', myformset.non_field_error())
                print('errors', myformset.errors)

        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

            data['orderitems'] = formset
        # ---------
        data['title'] = 'заказ/редактирование'
        return data

    def form_valid(self, form):

        print('Валидация формы')
        context = self.get_context_data()

        orderitems = context['orderitems']

        if any(orderitems.errors):
            print(self.object.id)
            # success_url = reverse_lazy(f'ordersapp:order_update {self.object.id}')
            print('orderitems.errors---->>>>', orderitems.errors)
            # return super(OrderItemsUpdate, self).form_valid(form)
            # return HttpResponseRedirect(reverse_lazy('ordersapp:order_update',
            #                                          kwargs={'pk': self.object.id}))
            return render_to_response('ordersapp/order_form.html', {'orderitems': orderitems})


        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


def order_ajax_price(request, pk, select_num):
    # print('я в order_ajax_price')
    # print(f'select_num - > {select_num} ')

    if request.is_ajax():
        # print('class_num ->', int(pk))
        # print('selectedIndex ->', select_num)
        # items = OrderItem.objects.all()
        # for k in items:
        #     print(k)
        #     print(k.id, k.product.name, k.product.id)

        # order_item_obj = OrderItem.objects.get(product__name=select_num)
        # print('product_price ->', order_item_obj)
        # print('product_price ->', order_item_obj.product.price)
        # print('product_id ->', order_item_obj.product.id)

        products = Product.objects.get(id=select_num - 1).select_related()
        # products = Product.objects.all()
        # product_price = products[select_num - 1].price
        product_price = products.price
        class_num = int(pk)
        content = {
            'product_price': product_price,
            'class_num': class_num,
        }

        result = render_to_string('ordersapp/includes/inc_boot_order.html', content)

        return JsonResponse({'result': result})


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
