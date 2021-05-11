from django.contrib import admin
from .models import *

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(OrderItem)