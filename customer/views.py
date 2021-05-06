from django.shortcuts import render
from django.views import View
from .models import *
from django.core.mail import send_mail
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from home.models import *
from django.shortcuts import redirect

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        handrail = MenuItem.objects.filter(category__name__contains='手すり')
        wheelchair = MenuItem.objects.filter(category__name__contains='車いす')
        bed = MenuItem.objects.filter(category__name__contains='ベット')

        context = {
            'handrail':handrail,
            'wheelchair':wheelchair,
            'bed':bed,
        }

        return render(request, 'customer/order.html', context)
    
    def post(self, request,*args,**kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        facility = request.POST.get('facility')

        order_items ={
            'items':[]
        }
        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data ={
                'id':menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }
            order_items['items'].append(item_data)

        price = 0
        item_ids =[]

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            phone=phone,
            facility=facility,
            )
        order.items.add(*item_ids)

        body = ('ご予約ありがとうございます。確認次第に相談員からのご連絡差し上げます。\n'
            f'合計：{price}\n'
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
            'items':order_items['items'],
            'price':price,
        }
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