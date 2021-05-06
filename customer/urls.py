from django.urls import path
from .views import *

urlpatterns = [
    path('about/', About.as_view(), name='about'),
    path('', Order.as_view(), name='order'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('notification/<int:notification_pk>/order/<int:order_pk>', OrderNotification.as_view(), name='order-notification'),
] 