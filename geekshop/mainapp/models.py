from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name="имя", unique=True)
    description = models.TextField(blank=True, verbose_name="описание")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='название продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='краткое описание продукта', max_length=60, blank=True)
    description = models.TextField(verbose_name='описание продукта',blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество на складе', default=0)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return f'{self.name} ({self.category.name})'



class Contacts(models.Model):
    name = models.CharField(max_length=64, verbose_name="название", unique=True)
    city= models.CharField(max_length=64, verbose_name="город")
    email = models.CharField(max_length=64, verbose_name="email", unique=True)
    phone = models.CharField(max_length=64, verbose_name="телефон", unique=True)
    adress = models.CharField(max_length=128, verbose_name="адрес", blank=True)

    class Meta:
        verbose_name = "контакты"
        verbose_name_plural = "контакты"


    def __str__(self):
        return f'{self.name} ({self.city})'


# создаем дамп данных , сохраняем в папаку fixture
# python manage.py dumpdata --format=json --indent 2 mainapp > mainapp/fixtures/db_dump1.json

# Загружаем файл фикстур в базу данных, django грузит файл из папаки mainapp/fixtures/
# python manage.py loaddata db_dump1