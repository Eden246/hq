from django.db import models
from django.urls.base import reverse_lazy
from django.contrib.auth.models import User
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', blank=True)
    price = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    video_url = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.name

    def get_remove_from_cart_url(self):
        return reverse_lazy("remove-from-cart", kwargs={
            'pk': self.pk
        })


class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(
        'MenuItem', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.items} | {self.quantity}件'

    @property
    def get_total_item_price(self):
        return int(self.quantity) * int(self.items.price)


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(
        'OrderItem')
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    facility = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_paid = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'カート生成日付:{self.created_on.strftime("%Y%m%d|%H:%M:%S")}'
