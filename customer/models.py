from django.db import models
from django.urls.base import reverse_lazy
from django.contrib.auth.models import User
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

class Tracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    category = models.ForeignKey('Category', related_name="tracker_category" ,on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    contract_image = models.ImageField(upload_to='contract_images/')
    type = models.CharField(max_length=100, default='在庫追加')

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
    license = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    facility = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(default=2)
    description = models.CharField(max_length=100, blank=True)
    permitter = models.ForeignKey(User, related_name='permitter', on_delete=models.CASCADE, blank=True, null=True)
    permit_day = models.DateTimeField(blank=True, null=True)
    handler = models.ForeignKey(User, related_name="handler", on_delete=models.CASCADE, blank=True, null=True)
    location_selecter = models.IntegerField(blank=True)
    limit = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.created_on.strftime("%Y%m%d")}｜{self.name}|{self.price}円'
