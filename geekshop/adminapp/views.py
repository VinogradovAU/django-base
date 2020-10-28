from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from authapp.models import ShopUser
from django.urls import reverse, reverse_lazy
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm
from adminapp.forms import ProductEditForm, ProductCategoryEditForm
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, DeleteView


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'update_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', content)


#
# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/жпользователи'
#     users_list = ShopUser.objects.all().order_by("-is_active")
#
#     content = {
#         'title': title,
#         'objects': users_list,
#     }
#     return render(request, 'adminapp/users.html', content)


class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': edit_form,
    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete_permanently(request, pk):
    title = 'удалить на всегда'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # вместо удаления лучше сделаем неактивным
        user.delete()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete_permanently.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_recovery(request, pk):
    title = 'пользователи/восстановление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_recovery.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    saccess_url = reverse_lazy('admin:categories')
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()

        return HttpResponseRedirect(reverse('admin:categories'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'

        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()

        return HttpResponseRedirect(reverse('admin:categories'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'

        return context


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_queryset(self):
        qs = super().get_queryset().order_by('-is_active')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print('context:', context)
        context['title'] = 'категории/список'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#     categories_list = ProductCategory.objects.all().order_by("-is_active")
#
#     content = {
#         'title': title,
#         'objects': categories_list,
#     }
#     return render(request, 'adminapp/categories.html', content)

class ProductCategoryDeteleView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryDeteleView, self).get_context_data()
        context['title'] = 'категории/удаление'
        return context



# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {'title': title, 'objects': category}
#
#     return render(request, 'adminapp/category_delete.html', content)

class ProductCategoryRecoveryView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_recovery.html'
    success_url = reverse_lazy('adminapp:categories')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()

        return self.get_success_url()

    def get_success_url(self):
        return HttpResponseRedirect(self.success_url)

# @user_passes_test(lambda u: u.is_superuser)
# def category_recovery(request, pk):
#     title = 'категории/восстановление'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         category.is_active = True
#         category.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {
#         'title': title,
#         'objects': category,
#     }
#
#     return render(request, 'adminapp/category_recovery.html', content)


class ProductView(DetailView):
    model = Product
    template_name = 'adminapp/prod.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    # fields = '__all__'
    form_class = ProductEditForm

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['pk'] = self.object.pk
        print(context)
        return context

    def get_initial(self):
        self.object = self.get_object()
        initial = super(ProductCreateView, self).get_initial()
        initial = initial.copy()
        initial['category'] = self.object.pk
        initial['name'] = ''
        initial['iamge'] = 'products_images/default.jpg'
        initial['short_desc'] = ''
        initial['description'] = ''
        initial['price'] = 0
        initial['quantity'] = 0
        initial['is_active'] = False
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return self.get_success_url()

    def get_success_url(self):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy('admin:products', kwargs={'pk': self.object.pk}))


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'товары/список'
        context['category_pk'] = self.kwargs['pk']
        return context

    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']
        qs = super().get_queryset().filter(category__pk=pk).order_by('-is_active')
        return qs


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk=None):
#     # выводим данные о продукте pk
#     title = 'админка/продукт'
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by("-is_active")
#
#     content = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', content)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('admin:products')

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return self.get_success_url()

    def get_success_url(self):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy('admin:products', kwargs={'pk': self.object.category.pk}))


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('adminapp:products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        # pk = self.object.category.pk

        return HttpResponseRedirect(reverse_lazy('admin:products', kwargs={'pk': self.object.category.pk}))

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['pk'] = self.object.pk
        return context


    def get_success_url(self):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy('admin:products', kwargs={'pk': self.object.pk}))

# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     pass
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     pass

class ProductRecoveryView(UpdateView):
    model = Product
    template_name = 'adminapp/product_recovery.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('admin:products')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return self.get_success_url()
    # def form_valid(self, form):
    #     # self.object = form.save(commit=True)
    #     self.object = self.get_object()
    #     self.object.is_active = True
    #     self.object.save()
    #     return self.get_success_url()

    def get_success_url(self):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy('admin:products', kwargs={'pk': self.object.category.pk}))