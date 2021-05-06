from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', blank=True)
    price = models.IntegerField()
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    facility = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'注文日付:{self.created_on.strftime("%Y%m%d|%H:%M:%S")}'

