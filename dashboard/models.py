from customer.models import OrderModel
from django.db import models
from django.contrib.auth.models import User
from home.models import *
from django.urls import reverse

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    order= models.ForeignKey(OrderModel, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=100, blank=True, null=True)
    result = models.IntegerField(default=3)
    image = models.ImageField(upload_to='contract_images/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('order_list')

class Text(models.Model):
    first = models.CharField(max_length=100, blank=True)
    second = models.CharField(max_length=100, blank=True)
    third = models.CharField(max_length=100, blank=True)
