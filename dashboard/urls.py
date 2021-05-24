from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard_order/', dashboard_order.as_view(), name='dashboard_order'),
    path('', dashboard,name='dashboard'),
    path('user/', user, name='user'),
    path('item/', item, name='item'),
    path('item/add/<int:pk>/', item_add, name='item_add'),
    path('item/delete/<int:pk>/', item_delete, name='item_delete'),
    path('item_save/', item_save, name='item_save'),
] 