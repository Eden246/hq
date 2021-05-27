from django.db.models.aggregates import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from customer.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.http.response import JsonResponse
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncDate
import datetime
from django.db.models import Q
from django.contrib.auth.models import User


@login_required
def order_list(request):
    orders = OrderModel.objects.filter(ordered=False, is_paid=False)
    total_revenue = 0
    for order in orders:
        total_revenue += order.price
    pie_data = []
    pie_label = []

    qs = OrderModel.objects.filter(ordered=False, is_paid=False).values(
        'items__items__category__parent').exclude(items__items__name__isnull=True).annotate(sum=Sum('items__quantity')).values('items__items__category__parent__name', 'sum')
    for i in qs:
        pie_label.append(i['items__items__category__parent__name'])
        pie_data.append(i['sum'])

    context = {
        'orders': orders,
        'total_orders': len(orders),
        'total_revenue': total_revenue,
        'pie_label': pie_label,
        'pie_data': pie_data,
    }

    return render(request, 'dashboard/order_list.html', context)


@login_required
def dashboard(request):
    today = datetime.date.today()
    labels = []
    data = []

    year = request.GET.get('year')
    month = request.GET.get('month')
    category = request.GET.get('category')

    if year != ' ' and year is not None and year != '今年' and month != ' ' and month is not None and month != '今月' and category != ' ' and category is not None and category == '全体':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year).annotate(create=TruncDate(
            'created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

    elif year != ' ' and year is not None and year != '今年' and month != ' ' and month is not None and month != '今月' and category != ' ' and category is not None and category != '全体':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year, items__items__category__parent=category).annotate(create=TruncDate(
            'created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

    elif year != ' ' and year is not None and year == '今年' and month != ' ' and month is not None and month == '今月' and category != ' ' and category is not None and category != '全体':
        qs = OrderModel.objects.filter(created_on__month=today.month, created_on__year=today.year, items__items__category__parent=category).annotate(create=TruncDate(
            'created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

    else:
        qs = OrderModel.objects.filter(created_on__month=today.month, created_on__year=today.year).annotate(
            create=TruncDate('created_on')).values('create').annotate(count=Count('items__items')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

    pie_data = []
    pie_label = []

    if year != ' ' and year is not None and year != '今年' and month != ' ' and month is not None and month != '今月':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year).values(
            'items__items__category__parent').exclude(items__items__name__isnull=True).annotate(total_price=Sum(F('items__items__price')*F('items__quantity'))).values('items__items__category__parent__name', 'total_price')

    else:
        qs = OrderModel.objects.filter(created_on__month=today.month, created_on__year=today.year).values(
            'items__items__category__parent').exclude(items__items__name__isnull=True).annotate(total_price=Sum(F('items__items__price')*F('items__quantity'))).values('items__items__category__parent__name', 'total_price')

    for i in qs:
        pie_label.append(i['items__items__category__parent__name'])
        pie_data.append(i['total_price'])

    bar_data = []
    bar_label = []

    if year != ' ' and year is not None and year != '今年' and month != ' ' and month is not None and month != '今月' and category != ' ' and category is not None and category == '全体':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')
        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    elif year != ' ' and year is not None and year != '今年' and month != ' ' and month is not None and month != '今月' and category != ' ' and category is not None and category != '全体':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year, items__items__category__parent=category).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')
        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    elif year != ' ' and year is not None and year == '今年' and month != ' ' and month is not None and month == '今月' and category != ' ' and category is not None and category != '全体':
        qs = OrderModel.objects.filter(created_on__month=today.month, created_on__year=today.year, items__items__category__parent=category).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')
        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    else:
        qs = OrderModel.objects.filter(created_on__month=today.month, created_on__year=today.year).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')

        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    return render(request, 'dashboard/dashboard.html', {
        'labels': labels,
        'data': data,
        'pie_label': pie_label,
        'pie_data': pie_data,
        'bar_label': bar_label,
        'bar_data': bar_data,
        'year': year,
        'month': month,
    })


@login_required
def user(request):
    if request.GET.get('query') != None:
        query = request.GET.get('query')
        users = User.objects.filter(
                Q(username__icontains=query)
            )
    else:
        users = User.objects.all()

    context = {
        'users': users,
    }
    return render(request, 'dashboard/user.html', context)


@login_required
def item(request):
    items = MenuItem.objects.all()
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
        'items': items.order_by('category__parent'),
        'form': form,
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
    if type == "category_parent":
        item.category.name = value
    if type == "category_name":
        item.category.name = value
    if type == "quantity":
        item.quantity = value
    if type == "price":
        item.price = value
    item.save()
    return JsonResponse({"success": "Updated"})
