from customer.models import OrderModel
from django.db import models
from django.contrib.auth.models import User

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    order= models.ForeignKey(OrderModel, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=100)
    result = models.IntegerField(default=3)
    comment = models.CharField(max_length=100, blank=True)