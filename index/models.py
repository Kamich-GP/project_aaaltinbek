from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=16, verbose_name='Название категории')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'категории'
        verbose_name = 'категорию'

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=128, verbose_name='Название продукта')
    product_des = models.TextField(verbose_name='Описание')
    product_count = models.IntegerField(verbose_name='Количество на складе')
    product_price = models.IntegerField(verbose_name='Цена')
    product_photo = models.ImageField(upload_to='media', verbose_name='Фото')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'продукты'
        verbose_name = 'продукт'

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user_id = models.IntegerField()
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_pr_amount = models.IntegerField()

    class Meta:
        verbose_name_plural = 'корзины'
        verbose_name = 'корзину'

    def __str__(self):
        return f'Корзина пользователя с ID {self.user_id}'
