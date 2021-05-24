from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from customer.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.http.response import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
import datetime

class dashboard_order(LoginRequiredMixin, UserPassesTestMixin, View):
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

        return render(request, 'dashboard/order.html',context)
    
    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()

@login_required
def dashboard(request):
    today = datetime.date.today()
    labels = []
    data = []
    data1 = []
    data2 = []

    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year != ' ' and year is not None and year != '年度を選択してください' and month != ' ' and month is not None and month != '当月を選択してください':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year).annotate(create=TruncDate('created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')  
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])
        
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year, items__items__category=1).annotate(create=TruncDate('created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')  
        for i in qs:
            data1.append(i['count'])
        
        qs2 = OrderModel.objects.filter(created_on__month=month, created_on__year=year, items__items__category=2).annotate(create=TruncDate('created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')  
        for i in qs2:
            data2.append(i['count'])
    else:
        qs = OrderModel.objects.filter(created_on__month=today.month, created_on__year=today.year).annotate(create=TruncDate('created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')  
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

        qs = OrderModel.objects.filter(created_on__month=today.month, created_on__year=today.year, items__items__category=1).annotate(create=TruncDate('created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')  
        for i in qs:
            data1.append(i['count'])

        qs2 = OrderModel.objects.filter(created_on__month=today.month, created_on__year=today.year, items__items__category=2).annotate(create=TruncDate('created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')  
        for i in qs2:
            data2.append(i['count'])

    return render(request, 'dashboard/dashboard.html', {
        'labels': labels,
        'data': data,
        'data1': data1,
        'data2': data2,
    })

@login_required
def user(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'dashboard/user.html', context)

@login_required
def item(request):
    items = MenuItem.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item')
        if request.POST.get('delete'):
            item.delete()
            return redirect('item')
    else:
        form = ItemForm()

    context = {
        'items' : items,
        'form':form,
    }
    return render(request, 'dashboard/item.html', context)

def item_add(self, pk):
    item = MenuItem.objects.get(pk=pk)
    item.quantity += 1
    item.save()
    return redirect('item')

def item_delete(self, pk):
    item = MenuItem.objects.get(pk=pk)
    if item.quantity > 0:
        item.quantity -= 1
        item.save()
        return redirect('item')
    else:
        item.delete()
        return redirect('item')

def confirm_choice():
    confirm = input("[c]confirm")
    if confirm != 'c':
        return item_delete


@csrf_exempt
def item_save(request):
    id = request.POST.get('id', '')
    type = request.POST.get('type', '')
    value = request.POST.get('value', '')
    item = MenuItem.objects.get(id=id)
    if type == "name":
        item.name = value
    if type == "category":
        item.category = value
    if type == "quantity":
        item.quantity = value
    if type == "price":
        item.price = value
    item.save()
    return JsonResponse({"success":"Updated"})