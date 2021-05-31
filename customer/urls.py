from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('', Order.as_view(), name='order'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('confirmation/<str:price>/<int:order_pk>', confirmation, name='confirmation'),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('notification/<int:notification_pk>/order/<int:order_pk>',OrderNotification.as_view(), name='order-notification'),
]
