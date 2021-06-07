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
from dashboard.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse

class Order(View):
    def get(self, request, *args, **kwargs):
        items_list = MenuItem.objects.filter(quantity__gt=0)
        categories = Category.objects.all()

        if request.user.is_authenticated:
            if OrderItem.objects.filter(user=request.user, ordered=False):
                order_item = OrderItem.objects.filter(
                    user=request.user, ordered=False)
            else:
                order_item = None
        else:
            order_item = None

        name = request.GET.get('name')
        detail = request.GET.get('detail')
        category = request.GET.get('category')
        maxPrice = request.GET.get('maxPrice')

        if name != ' ' and name is not None:
            items_list = items_list.filter(name__icontains=name)

        if detail != ' ' and detail is not None:
            items_list = items_list.filter(description__icontains=detail)

        if maxPrice != ' ' and maxPrice is not None:
            items_list = items_list.filter(price__range=(0, maxPrice))
        if category != ' ' and category is not None and category != '全ての品目':
            items_list = items_list.filter(category__name__icontains=category)

        price = 0
        if request.user.is_authenticated:
            if OrderItem.objects.filter(user=request.user, ordered=False):
                for item in order_item:
                    price += item.get_total_item_price

        page = request.GET.get('page', 1)
        paginator = Paginator(items_list.order_by('category__parent'), 4)
        items = paginator.page(page)

        context = {
            'order_item': order_item,
            'price': price,
            'items': items,
            'categories': categories
        }

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        item = request.POST.get('items[]')
        menu_item = MenuItem.objects.get(pk__contains=int(item))
        if OrderItem.objects.filter(user=request.user, items=menu_item, ordered=False):
            order_item = OrderItem.objects.filter(
                user=request.user, items=menu_item, ordered=False)[0]
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "カートに追加されました。")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.info(request, "カートに追加されました。")
            OrderItem.objects.create(
                user=request.user, items=menu_item, ordered=False).save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_from_cart(request, pk):
    menu_item = get_object_or_404(MenuItem, id=pk)
    order_item = OrderItem.objects.filter(
        user=request.user, items=menu_item, ordered=False)[0]
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
        messages.info(request, "品目の数量が減りました。")
        return redirect("order")
    else:
        order_item.delete()
        messages.info(request, "品目が削除されました。")
        return redirect("order")


class CartView(View):
    def get(self, request, *args, **kwargs):
        order_item = OrderItem.objects.filter(user=request.user, ordered=False)

        price = 0
        for item in order_item:
            price += item.get_total_item_price

        context = {
            'items': order_item,
            'price': price,
        }
        return render(request, 'customer/cart.html', context)

    def post(self, request, *args, **kwargs):
        order_item = OrderItem.objects.filter(user=request.user, ordered=False)

        item_ids = []
        for item in order_item:
            item_ids.append(item.id)

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        facility = request.POST.get('facility')
        license = request.POST.get('license')

        price = 0
        for item in order_item:
            price += item.get_total_item_price

        order_item.update(ordered=True)

        order = OrderModel.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            facility=facility,
            price=price,
            license=license,
        )
        order.items.add(*item_ids)

        items =[]
        for item in order.items.all():
            items.append(item)

        user_limit, created = Limit.objects.get_or_create(user=request.user)
        user_limit.limit -= price
        user_limit.save(update_fields=['limit'])

        body = (f'{facility}の{name}様、只今ご予約承りました！\n確認が終わる次第に津営業所の相談員がこちらの番号（{phone}）でご連絡差し上げます。\n'
                f'品目リスト：{items}\n合計：{price}\n'
                )
        # import smtplib
        # from email.mime.text import MIMEText

        # to_email = "so-kan@life-techno.jp"
        # from_email = "tsu-watase@life-techno.jp"

        # # MIMETextを作成
        # message = body
        # msg = MIMEText(message, "html")
        # msg["Subject"] = f'{facility}の{name}様、ライフテクノサービス（津営業所）予約完了メール'
        # msg["To"] = email
        # msg["From"] = "so-kan@life-techno.jp"

        # # サーバを指定する
        # server = smtplib.SMTP("118.21.150.161", 587)
        # # メールを送信する
        # server.send_message(msg)
        # # 閉じる
        # server.quit()

        # send_mail(
        #     f'{facility}の{name}様、ライフテクノサービス（津営業所）予約完了メール',
        #     body,
        #     'ライフテクノサービス・レンタル事業部<so-kan@life-techno.jp>',
        #     [email,'so-kan@life-techno.jp'],
        #     fail_silently= False
        # )
        staffs = User.objects.filter(groups__name__in=['staff'])
        for staff in staffs:
            notification = Notification.objects.create(
                notification_type=4, from_user=request.user, to_user=staff, order=order)

        return HttpResponseRedirect(reverse('confirmation', kwargs={'order_pk':order.pk}))

def confirmation(request, order_pk):
    order = OrderModel.objects.get(pk=order_pk)
    return render(request, 'customer/order_confirmation.html', {'order':order})

class OrderNotification(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, notification_pk, order_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        order = OrderModel.objects.get(pk=order_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('order-detail', pk=order_pk)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()
