from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class News(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='main/', blank=True, null=True)
    description = RichTextField(blank=True)  # Заменяем TextField на RichTextField
    published_at = models.DateTimeField()

    def __str__(self):
        return self.name

class Actions(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='main/', blank=True, null=True)
    description = RichTextField(blank=True)
    published_at = models.DateTimeField()
    start_date = models.DateTimeField()  # Дата начала акции
    end_date = models.DateTimeField()  # Дата конца акции

    def __str__(self):
        return self.name

    @property
    def time_left(self):
        # Рассчитываем сколько времени осталось до конца акции
        remaining_time = self.end_date - timezone.now()
        if remaining_time.total_seconds() > 0:
            return remaining_time
        else:
            return "Акция завершена"
        
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Позволяем пустые значения

    def get_total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.get_total_price()
        return total
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)

    def get_product_name(self):
        return self.content_object.name  # Имя продукта

    def get_product_image_url(self):
        if self.content_object.image:  # Проверяем, есть ли изображение
            return self.content_object.image.url
        else:
            return '/media/goods/placeholder.jpg'  # Укажите путь к изображению по умолчанию

    def get_total_price(self):
        return self.content_object.price * self.quantity  # Общая цена
    

class Company(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='main/', blank=True, null=True)
    description = RichTextField(blank=True)  # Заменяем TextField на RichTextField

    def __str__(self):
        return self.name