from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(MessageModel)
