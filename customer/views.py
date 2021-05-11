from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import *
from django.core.mail import send_mail
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from home.models import *
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class Order(View):
    def get(self, request, *args, **kwargs):
        items_list = MenuItem.objects.all()
        categories = Category.objects.all()
        unorders = OrderItem.objects.filter(user=request.user, ordered=False)
        unpaid_orders = OrderModel.objects.filter(user=request.user, is_paid=False)

        category = request.GET.get('category')
        
        if category != ' ' and category is not None and category != '選択してください':
            items_list = items_list.filter(category__name__icontains=category)
        
        page = request.GET.get('page', 1)
        paginator = Paginator(items_list, 2)
        items = paginator.page(page)

            
        context = {
            'unorders': unorders,
            'unpaid_orders': unpaid_orders[0],
            'items':items,
            'categories':categories
        }

        return render(request, 'customer/order.html', context)
    
    def post(self, request,*args,**kwargs):
        item = request.POST.get('items[]')
        menu_item = MenuItem.objects.get(pk__contains=int(item))
        order_item, created = OrderItem.objects.get_or_create(user=request.user, items=menu_item,ordered=False)
        unpaid_orders = OrderModel.objects.filter(user=request.user, is_paid=False)
        if unpaid_orders.exists():
            order = unpaid_orders[0]
            if order.items.filter(items=menu_item).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "カートに追加されました。")
                return redirect("order")
            else:
                messages.info(request, "カートに追加されました。")
                order.items.add(order_item)
                return redirect("order")
        else:
            order = OrderModel.objects.create(user=request.user)
            order.items.add(order_item)
            return redirect("order")

@login_required
def remove_from_cart(request, pk):
    menu_item = get_object_or_404(MenuItem, id=pk)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, items=menu_item,ordered=False)
    unpaid_orders = OrderModel.objects.filter(user=request.user, is_paid=False)
    if unpaid_orders.exists():
        order = unpaid_orders[0]
        if order.items.filter(items=menu_item).exists():
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "品目の数量が減りました。")
                return redirect("order")
            else:
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "品目が削除されました。")
                return redirect("order")
        else:
            return redirect("order")
    else:
        return redirect("order")

class CartView(View):
    def get(self, request, *args, **kwargs):
        unpaid_orders = OrderModel.objects.filter(user=request.user, is_paid=False)
        context = {
            'items':unpaid_orders[0].items.all(),
            'unpaid_orders':unpaid_orders[0],
        }
        return render(request, 'customer/cart.html', context)
    
    def post(self, request, *args, **kwargs):
        unpaid_orders = OrderModel.objects.filter(user=request.user, is_paid=False)
        items = unpaid_orders[0].items.all()
        
        item_ids = []
        for item in items:
            item_ids.append(item.id)

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        facility = request.POST.get('facility')

        price = 0
        for item in items:
            price += item.get_total_item_price

        order = OrderModel.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            facility=facility,
            price=price,
            )
        order.items.add(*item_ids)
        
        body = ('ご予約ありがとうございます。確認次第に相談員からのご連絡差し上げます。\n'
            f'合計：\n'
        )

        send_mail(
            'ご予約ありがとうございます。',
            body,
            'example@example.com',
            [email],
            fail_silently= False
        )
        staffs = User.objects.filter(groups__name__in=['staff'])
        for staff in staffs:
            notification = Notification.objects.create(notification_type=4, from_user=request.user, to_user=staff, order=order)
        
        context = {
            'price':price,
        }

        delete_orders = unpaid_orders[0].items.all()
        delete_orders.delete()

        return render(request, 'customer/order_confirmation.html',context)

class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order' : order
        }
        return render(request, 'customer/order-detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_paid = True
        order.save()
        context = {
            'order':order,
        }
        return render(request, 'customer/order-detail.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()

class OrderNotification(LoginRequiredMixin, UserPassesTestMixin,View):
    def get(self, request, notification_pk, order_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        order = OrderModel.objects.get(pk=order_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('order-detail', pk=order_pk)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()

def add_to_cart(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    order_item = OrderItem.objects.create(item=item)
    unpaid_orders = OrderModel.objects.filter(user=request.user, is_paid=False)
    if unpaid_orders.exists():
        order = unpaid_orders[0]
        if order.items.filter(item__pk = item.pk).exists():
            order_item.quantity += 1
            order_item.save()
    else:
        order = OrderModel.objects.create(user=request.user)
        order.items.add(order_item)
    return redirect("order")