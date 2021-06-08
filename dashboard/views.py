from django.db.models.aggregates import Sum
from django.http import response
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from customer.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.http.response import HttpResponse, JsonResponse
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncDate
import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponseRedirect

def chart(request):
    today = datetime.date.today()
    labels = []
    data = []
    year = request.GET.get('year')
    month = request.GET.get('month')
    category = request.GET.get('category')

    if year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month != '指定なし' and category != ' ' and category is not None and category != '指定なし':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year, items__items__category__parent=category).annotate(create=TruncDate(
            'created_on')).values('create').annotate(count=Sum('items__quantity')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

    elif year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month != '指定なし' and category != ' ' and category is not None and category == '指定なし':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year).annotate(create=TruncDate(
            'created_on')).values('create').annotate(count=Sum('items__quantity')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

    elif year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month == '指定なし' and category != ' ' and category is not None and category != '指定なし':
        qs = OrderModel.objects.filter(created_on__year=year, items__items__category__parent=category).annotate(create=TruncDate(
            'created_on')).values('create').annotate(count=Sum('items__quantity')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

    elif year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month == '指定なし' and category != ' ' and category is not None and category == '指定なし':
        qs = OrderModel.objects.filter(created_on__year=year).annotate(create=TruncDate(
            'created_on')).values('create').annotate(count=Sum('items__quantity')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])


    elif year != ' ' and year is not None and year == '指定なし' and month != ' ' and month is not None and month == '指定なし' and category != ' ' and category is not None and category != '指定なし':
        qs = OrderModel.objects.filter(created_on__year=today.year, items__items__category__parent=category).annotate(create=TruncDate(
            'created_on')).values('create').annotate(count=Sum('items__quantity')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

    else:
        qs = OrderModel.objects.filter(created_on__lte=datetime.datetime.today(), created_on__gt=datetime.datetime.today()-datetime.timedelta(days=30)).annotate(create=TruncDate(
            'created_on')).values('create').annotate(count=Sum('items__quantity')).values('create', 'count')
        for i in qs:
            labels.append(i['create'].strftime('%Y/%m/%d'))
            data.append(i['count'])

    pie_data = []
    pie_label = []

    if year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month != '指定なし':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year).values(
            'items__items__category__parent').exclude(items__items__name__isnull=True).annotate(total_price=Sum(F('items__items__price')*F('items__quantity'))).values('items__items__category__parent__name', 'total_price')

    elif year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month == '指定なし':
        qs = OrderModel.objects.filter(created_on__year=year).values(
            'items__items__category__parent').exclude(items__items__name__isnull=True).annotate(total_price=Sum(F('items__items__price')*F('items__quantity'))).values('items__items__category__parent__name', 'total_price')

    else:
        qs = OrderModel.objects.filter(created_on__lte=datetime.datetime.today(), created_on__gt=datetime.datetime.today()-datetime.timedelta(days=30)).values(
            'items__items__category__parent').exclude(items__items__name__isnull=True).annotate(total_price=Sum(F('items__items__price')*F('items__quantity'))).values('items__items__category__parent__name', 'total_price')

    for i in qs:
        pie_label.append(i['items__items__category__parent__name'])
        pie_data.append(i['total_price'])

    bar_data = []
    bar_label = []

    if year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month != '指定なし' and category != ' ' and category is not None and category == '指定なし':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')
        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    elif year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month != '指定なし' and category != ' ' and category is not None and category != '指定なし':
        qs = OrderModel.objects.filter(created_on__month=month, created_on__year=year, items__items__category__parent=category).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')
        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    elif year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month == '指定なし' and category != ' ' and category is not None and category == '指定なし':
        qs = OrderModel.objects.filter(created_on__year=year).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')
        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    elif year != ' ' and year is not None and year != '指定なし' and month != ' ' and month is not None and month == '指定なし' and category != ' ' and category is not None and category != '指定なし':
        qs = OrderModel.objects.filter(created_on__year=today.year, items__items__category__parent=category).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')
        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    elif year != ' ' and year is not None and year == '指定なし' and month != ' ' and month is not None and month == '指定なし' and category != ' ' and category is not None and category != '指定なし':
        qs = OrderModel.objects.filter(created_on__year=today.year, items__items__category__parent=category).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')
        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    else:
        qs = OrderModel.objects.filter(created_on__lte=datetime.datetime.today(), created_on__gt=datetime.datetime.today()-datetime.timedelta(days=30)).values(
            'items__items__name').exclude(items__items__name__isnull=True).annotate(items__quantity=Sum('items__quantity')).values('items__items__name', 'items__quantity')

        for i in qs:
            bar_label.append(i['items__items__name'])
            bar_data.append(i['items__quantity'])

    context = {
        'labels': labels,
        'data': data,
        'pie_label': pie_label,
        'pie_data': pie_data,
        'bar_label': bar_label,
        'bar_data': bar_data,
        'year': year,
        'month': month,
    }
    return render(request, 'dashboard/chart.html', context)

def paper(request, pk):
    order = OrderModel.objects.get(pk=pk)
    permissions = Permission.objects.filter(order__name=order.name).exclude(order__handler=None)
    context = {
        'order': order,
        'permissions': permissions,
    }
    return render(request, 'dashboard/paper.html', context)

class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }
        return render(request, 'dashboard/order-detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.status = 1
        order.handler = request.user
        order.save()
        message = request.POST.get('message', None)
        permission = Permission.objects.create(
            message=message,
            order=order,
            user=request.user,
        )
        permission.save()
        
        return HttpResponseRedirect(reverse_lazy("permission"))

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()

def profile(request, pk):
    user = User.objects.get(pk=pk)
    context = {
        'user':user
    }
    return render(request, 'dashboard/profile.html', context)

def image(request, pk):
    permission = Permission.objects.get(pk=pk)
    form = ImageForm(request.POST or None, request.FILES or None,  instance=permission)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
        permission.result = 1
        permission.save()
        for i in permission.order.items.all():
            permission_quantity = i.quantity
            menu_item = MenuItem.objects.get(pk=i.items.pk)
            menu_item.quantity -= permission_quantity
            menu_item.save()
            Tracker.objects.create(
                name = menu_item.name,
                quantity = permission_quantity,
                user = request.user,
                type= "貸出",
                category = menu_item.category,
                contract_image = form.cleaned_data['image']
            )
    # return render(request, 'dashboard/image.html', {'i':items})
    return HttpResponseRedirect(reverse_lazy("permission"))
    
def image(request, pk):
    permission = Permission.objects.get(pk=pk)
    form = ImageForm(request.POST or None, request.FILES or None,  instance=permission)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
        permission.result = 1
        permission.save()
        for i in permission.order.items.all():
            permission_quantity = i.quantity
            menu_item = MenuItem.objects.get(pk=i.items.pk)
            menu_item.quantity -= permission_quantity
            menu_item.save()
            Tracker.objects.create(
                name = menu_item.name,
                quantity = permission_quantity,
                user = request.user,
                type= "貸出",
                category = menu_item.category,
                contract_image = form.cleaned_data['image']
            )
    # return render(request, 'dashboard/image.html', {'i':items})
    return HttpResponseRedirect(reverse_lazy("permission"))

def permission(request):
    if request.method == 'POST':
        start = request.POST.get('fromdate', None)
        end = request.POST.get('todate', None)
        if start and end:
            permissions = Permission.objects.filter(date__lte=end, date__gt=start)
        else:
            permissions = Permission.objects.all()
    else:
        permissions = Permission.objects.all()

    text = Text.objects.first()
    form1 = ImageForm()
    context ={
        'permissions':permissions,
        'text':text,
        'form1':form1,
    }
    return render(request, 'dashboard/permission.html', context)

def approve(request, pk):
    today = datetime.datetime.now()
    permission = Permission.objects.get(pk=pk)
    permission.result = 0
    permission.save()
    order = OrderModel.objects.get(pk=permission.order.pk)
    order.status = 0
    order.permitter = request.user
    order.permit_day = today
    order.save()
    return redirect('permission')

def disapprove(request, pk):
    permission = Permission.objects.get(pk=pk)
    permission.delete()
    order = OrderModel.objects.get(pk=permission.order.pk)
    order.status = 2
    order.save()
    return redirect('permission')

def back(request, pk):
    permission = Permission.objects.get(pk=pk)
    permission.result = 2
    permission.save()
    order = OrderModel.objects.get(pk=permission.order.pk)
    order.status = 0
    order.save()
    form0 = TrackerImageForm(request.POST, request.FILES)
    for i in order.items.all():
        Tracker.objects.create(
            user=request.user,
            name=i.items.name,
            type= 1,
            quantity = i.quantity,
            category = i.itmes.category,
            contract_image = form0.cleaned_data['contract_image']
        )

    return redirect('permission')

def not_back(request, pk):
    pk = request.POST.get('pk', '')
    permission = Permission.objects.get(pk=pk)
    permission.delete()
    order = OrderModel.objects.get(pk=permission.order.pk)
    order.status = 2
    order.save()
    return redirect('permission')

@csrf_exempt
def permission_save(request):
    id = request.POST.get('id', '')
    type = request.POST.get('type', '')
    value = request.POST.get('value', '')
    permission = Permission.objects.get(id=id)
    if type == "comment":
        permission.comment = value
    permission.save()
    return JsonResponse({"success": "Updated"})

@login_required
def order_list(request):
    orders = OrderModel.objects.filter(status=2)
    total_revenue = 0
    for order in orders:
        total_revenue += order.price
    pie_data = []
    pie_label = []

    qs = orders.values('items__items__category__parent').exclude(items__items__name__isnull=True).annotate(sum=Sum('items__quantity')).values('items__items__category__parent__name', 'sum')
    for i in qs:
        pie_label.append(i['items__items__category__parent__name'])
        pie_data.append(i['sum'])

    text = Text.objects.first()
    text_form= TextForm(request.POST or None, instance = text)
    if text_form.is_valid():
        text_form.save()

    if request.method == 'POST':
        form0 = TrackerImageForm(request.POST, request.FILES)
        permission_pk = request.POST.get('permission_pk')
        permission = Permission.objects.get(pk=permission_pk)
        permission.result = 2
        permission.save()
        order = OrderModel.objects.get(pk=permission.order.pk)
        order.status = 0
        order.save()
        form0 = TrackerImageForm(request.POST, request.FILES)
        if form0.is_valid():
            for i in order.items.all():
                Tracker.objects.create(
                    user=request.user,
                    name=i.items.name,
                    type= "返品",
                    quantity = i.quantity,
                    category = i.items.category,
                    contract_image = form0.cleaned_data['contract_image']
                )
    else:
         form0 = TrackerImageForm()

    permissions = Permission.objects.filter(result=1)
    context = {
        'orders': orders,
        'total_orders': len(orders),
        'total_revenue': total_revenue,
        'pie_label': pie_label,
        'pie_data': pie_data,
        'text':text,
        'text_form':text_form,
        'form0':form0,
        'permissions':permissions,
    }

    return render(request, 'dashboard/order_list.html', context)

def test_func(user):
    return user.groups.filter(name='staff').exists()

@user_passes_test(test_func, login_url="/login/")
def dashboard(request):
    orders = OrderModel.objects.all().order_by('-created_on')[:5]
    users = User.objects.filter(permission__date__lte=datetime.datetime.today(), permission__date__gt=datetime.datetime.today()-datetime.timedelta(days=30), permission__result=1).annotate(total_price=Sum(F('permission__order__items__items__price')*F('permission__order__items__quantity'))).annotate(sum=Sum('permission__order__items__quantity')).values('username', 'sum', 'total_price').order_by('-total_price')[:5]
    text = Text.objects.first()
    text_form = TextForm(request.POST or None, instance = text)
    if text_form.is_valid():
        text_form.save()
    order_count = OrderModel.objects.filter(status=2).count()
    permission_count = Permission.objects.all().count()

    context = {
        'orders': orders,
        'users': users,
        'text':text,
        'text_form': text_form,
        'order_count': order_count,
        'permission_count':permission_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


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

import csv
import io
def item_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="list.csv"'
    sio = io.StringIO()
    writer = csv.writer(sio)
    writer.writerow(["登録者","お名前","数量","カテゴリー","カテゴリー詳細","登録日付"])
    for i in Tracker.objects.all().values_list("user","name","quantity","category__parent__name","category__name","created_on"):
        writer.writerow(i)
    response.write(sio.getvalue().encode('utf_8_sig'))
    return response

@login_required
def item(request):
    items = MenuItem.objects.all()
    trackers = Tracker.objects.all()
    permissions = Permission.objects.filter(result=1).order_by('-date')
    text = Text.objects.first()
    text_form = TextForm(request.POST or None, instance = text)
    if text_form.is_valid():
        text_form.save()
    if request.method == 'POST':
        if 'save_new' in request.POST:
            form0 = TrackerImageForm(request.POST, request.FILES)
            form = ItemForm(request.POST, request.FILES)
            if form0.is_valid():
                if form.is_valid():
                    form.save()
                    name =form.cleaned_data['name']
                    category =form.cleaned_data['category']
                    quantity =form.cleaned_data['quantity']
                    contract_image = form0.cleaned_data['contract_image']
                    Tracker.objects.create(
                        name=name, category=category, quantity=quantity, contract_image=contract_image,
                    )
                    return redirect('item')
        if 'save_renew' in request.POST:
            form0 = TrackerImageForm(request.POST, request.FILES)
            if form0.is_valid():
                item_id = request.POST.get('items[]')
                type = request.POST.get('type')
                quantity = request.POST.get('quantity')
                item = MenuItem.objects.get(pk=item_id)
                Tracker.objects.create(
                    user = request.user,
                    type= type,
                    name = item.name,
                    category = item.category,
                    quantity = quantity,
                    contract_image = form0.cleaned_data['contract_image']
                )
                item.quantity += int(quantity)
                item.save()
                return redirect('item')
    else:
        form0 = TrackerImageForm(request.POST, request.FILES)
        form = ItemForm()

    context = {
        'items': items.order_by('category__parent'),
        'form': form,
        'form0': form0,
        'text':text,
        'text_form':text_form,
        'permissions':permissions,
        'trackers':trackers
    }
    return render(request, 'dashboard/item.html', context)

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
