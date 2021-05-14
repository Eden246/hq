from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import *

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day, ordered=True, is_paid=False)

        unpaid_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.get_total()

            if not order.is_paid:
                unpaid_orders.append(order)

        context = {
            'orders': unpaid_orders,
            'total_revenue': total_revenue,
            'total_orders' : len(orders),
        }

        return render(request, 'dashboard/dashboard.html',context)
    
    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()