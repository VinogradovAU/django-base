from django import forms
from django.core.exceptions import ValidationError
from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):

        super(OrderItemForm, self).clean()
        if any(self.errors):
            return self.errors
        # print(self.cleaned_data['order'])
        # print(self.cleaned_data['product'])
        # print(self.cleaned_data['product'].quantity)
        # print(self.cleaned_data['id'])
        # print(self.cleaned_data['quantity'])
        # print('self.fields----->', self.fields.items())

        if self.cleaned_data['product'].quantity == 0:
            # self.add_error(self.fields['quantity'], '000000нет на складе')
            # print('Ошибка 1 формы')
            raise ValidationError(f"Товара {self.cleaned_data['product']} нет на складе")

        if self.cleaned_data['quantity'] > self.cleaned_data['product'].quantity:
            # print('quantity->', self.cleaned_data['quantity'])
            # self.add_error('quantity', 'OOOOOOOOOOOshibka')
            # print('Ошибка 2 формы')
            # print('product + quantity->', self.cleaned_data['product'].quantity)
            raise ValidationError(f"Товара {self.cleaned_data['product']} на складе {self.cleaned_data['product'].quantity} шт.")

        print(self.cleaned_data)
        # print(self.non_form_errors)

        return self.cleaned_data
