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
from django.core.paginator import Paginator


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
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    form = ImageForm(request.POST or None, request.FILES or None,  instance=permission)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
        permission.result = 1
        permission.start_date = start_date
        permission.end_date = end_date
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
    return HttpResponseRedirect(reverse_lazy("order_list"))

def updateimage(request, pk):
    permission = Permission.objects.get(pk=pk)
    end_date = request.POST.get('end_date')
    form = ImageForm(request.POST or None, request.FILES or None,  instance=permission)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
        permission.end_date = end_date
        permission.save()
    return HttpResponseRedirect(reverse_lazy("order_list"))
    
def return_image(request, pk):
    permission = Permission.objects.get(pk=pk)
    form = ImageForm(request.POST or None, request.FILES or None,  instance=permission)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
        permission.result = 2
        permission.save()
        for i in permission.order.items.all():
            permission_quantity = i.quantity
            menu_item = MenuItem.objects.get(pk=i.items.pk)
            menu_item.quantity += permission_quantity
            menu_item.save()
            Tracker.objects.create(
                name = menu_item.name,
                quantity = permission_quantity,
                user = request.user,
                type= "返品",
                category = menu_item.category,
                contract_image = form.cleaned_data['image']
            )
    return HttpResponseRedirect(reverse_lazy("order_list"))

def permission(request):
    result = request.GET.get('result')
    fromdate = request.GET.get('fromdate')
    todate = request.GET.get('todate')

    unpermission = Permission.objects.filter(result=0) | Permission.objects.filter(result=3)

    if result != '' and result is not None:
        unpermission = Permission.objects.filter(result=result)

    if fromdate != '' and fromdate is not None and todate != ' ' and todate is not None:
        unpermission = Permission.objects.filter(start_date__gte=fromdate).filter(end_date__lte=todate)

    uncharged = Permission.objects.filter(result=3)
    uncontract = Permission.objects.filter(result=0)
    form1 = ImageForm()

    context ={
        'uncharged': len(uncharged),
        'uncontract': len(uncontract),
        'unpermission':unpermission,
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
    return redirect('order_list')

def disapprove(request, pk):
    permission = Permission.objects.get(pk=pk)
    permission.delete()
    order = OrderModel.objects.get(pk=permission.order.pk)
    order.status = 2
    order.save()
    return redirect('order_list')

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

    return redirect('order_list')

def not_back(request, pk):
    pk = request.POST.get('pk', '')
    permission = Permission.objects.get(pk=pk)
    permission.delete()
    order = OrderModel.objects.get(pk=permission.order.pk)
    order.status = 2
    order.save()
    return redirect('order_list')

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

def book_list(request):
    orders = OrderModel.objects.filter(status=2)
    if request.method == 'POST':
            order_pk = request.POST.get('order_pk')
            order = OrderModel.objects.get(pk=order_pk)
            order.status = 1
            order.handler = request.user
            order.save()
            message = request.POST.get('message', None)
            permission = Permission.objects.create(
                message=message,
                order=order,
                user=request.user,
            )
            return redirect(reverse_lazy('permission'))
    return render(request, 'dashboard/book_list.html', {'orders': orders})

@login_required
def order_list(request):
    paginate_by = 2
    context = {}
    permission_list = Permission.objects.filter(Q(result=1) or Q(result=2))

    result1 = request.GET.get('result1')
    name = request.GET.get('name')
    user = request.GET.get('user')
    handler = request.GET.get('handler')
    if request.GET.get('startdate'):
        startdate = request.GET.get('startdate')
    else:
        startdate = datetime.datetime.today()-datetime.timedelta(days=9999)
    if request.GET.get('enddate'):
        enddate = request.GET.get('enddate')
    else:
        enddate = datetime.datetime.today()+datetime.timedelta(days=9999)
    
    if result1 or name or user or handler:
        permission_list = Permission.objects.filter(Q(start_date__gte=startdate) and Q(end_date__lte=enddate)).filter(result=result1).filter(order__name__icontains=name).filter(order__user__username__icontains=user).filter(user__username__icontains=handler)

    context['is_paginated'] = True
    paginator = Paginator(permission_list, paginate_by)
    page_number_range = 10
    current_page = int(request.GET.get('page',1))
    context['current_page'] = current_page

    start_index = int((current_page-1)/page_number_range)*page_number_range
    end_index = start_index + page_number_range
    current_page_group_range = paginator.page_range[start_index:end_index]
    start_page = paginator.page(current_page_group_range[0])
    end_page = paginator.page(current_page_group_range[-1])
    has_previous_page = start_page.has_previous()
    has_next_page = end_page.has_next()

    context['current_page_group_range'] = current_page_group_range
    if has_previous_page:
        context['has_previous_page'] = has_previous_page
        context['previous_page'] = start_page.previous_page_number
    if has_next_page:
        context['has_next_page'] = has_next_page
        context['next_page'] = end_page.next_page_number

    e = paginate_by * current_page
    s = e - paginate_by
    permission_list = permission_list[s:e]
    context['permissions'] = permission_list

    if request.method == 'POST':
        order_pk = request.POST.get('order_pk')
        order = OrderModel.objects.get(pk=order_pk)
        order.status = 1
        order.handler = request.user
        order.save()
        message = request.POST.get('message', None)
        permission = Permission.objects.create(
            message=message,
            order=order,
            user=request.user,
        )
        permission_pk = request.POST.get('permission_pk')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        permission = Permission.objects.get(pk=permission_pk)
        permission.result = 2
        permission.start_date = start_date
        permission.end_date = end_date
        permission.save()
        order = OrderModel.objects.get(pk=permission.order.pk)
        order.status = 0
        order.save()
        form0 = TrackerImageForm(request.POST, request.FILES)
    else:
        form0 = TrackerImageForm()
        context['form0'] = form0
        form = ImageForm()
        context['form'] = form

    return render(request, 'dashboard/order_list.html', context)



def test_func(user):
    return user.groups.filter(name='staff').exists()

@user_passes_test(test_func, login_url="/login/")
def dashboard(request):
    orders = OrderModel.objects.all().order_by('-created_on')[:10]
    users = User.objects.filter(permission__date__lte=datetime.datetime.today(), permission__date__gt=datetime.datetime.today()-datetime.timedelta(days=30), permission__result=1).annotate(total_price=Sum(F('permission__order__items__items__price')*F('permission__order__items__quantity'))).annotate(sum=Sum('permission__order__items__quantity')).values('username', 'sum', 'total_price').order_by('-total_price')[:10]
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
def recent_item_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="list.csv"'
    sio = io.StringIO()
    writer = csv.writer(sio)
    writer.writerow(["登録者","お名前","数量","カテゴリー","カテゴリー詳細","登録日付"])
    for i in Tracker.objects.filter(created_on__gte=datetime.datetime.today()-datetime.timedelta(days=30)).values_list("user","name","quantity","category__parent__name","category__name","created_on"):
        writer.writerow(i)
    response.write(sio.getvalue().encode('utf_8_sig'))
    return response

@login_required
def item(request):
    items = MenuItem.objects.all()
    tranker_list = Tracker.objects.all().order_by('-created_on')
    permissions = Permission.objects.filter(result=1).order_by('-date')
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

    page = request.GET.get('page', 1)
    paginator = Paginator(tranker_list.order_by('category__parent'), 10)
    trackers = paginator.page(page)
    context = {
        'items': items.order_by('category__parent'),
        'form': form,
        'form0': form0,
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
