from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from customer.models import *

class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    facility = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.user}+{self.facility}"

class Post(models.Model):
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    image = models.ManyToManyField("Image", blank=True)

class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent  = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

class Notification(models.Model):
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    message = models.ForeignKey('MessageModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='+', blank=True, null=True)

class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, related_name='+',blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    it_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
    image = models.ImageField(upload_to='images', blank=True, null=True)