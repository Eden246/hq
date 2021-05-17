from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from customer.models import *

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        orders = OrderModel.objects.filter(ordered=True, is_paid=False)

        total_revenue = 0

        for order in orders:
            total_revenue += order.price

        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders' : len(orders),
        }

        return render(request, 'dashboard/dashboard.html',context)
    
    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()