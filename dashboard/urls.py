from django.urls import path
from .views import *

urlpatterns = [
    path('order_list/', order_list, name='order_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('', dashboard, name='dashboard'),
    path('user/', user, name='user'),
    path('image/<int:pk>/', image, name='image'),
    path('permission/', permission, name='permission'),
    path('permission/approve/<int:pk>/', approve, name='approve'),
    path('permission/disapprove/<int:pk>/', disapprove, name='disapprove'),
    path('permission_save/', permission_save, name='permission_save'),
    path('item/', item, name='item'),
    path('item/csv', item_csv, name='item_csv'),
    path('item/delete/<int:pk>/', item_delete, name='item_delete'),
    path('item_save/', item_save, name='item_save'),
    path('paper/<int:pk>/', paper, name='paper'),
]
