from django.contrib import admin
from django.urls import path, include
from home.views import *
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='home'),
    path('signup/', SignupView,name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('post/', PostView.as_view(),name='post'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name='post_edit'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>', CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
    path('profile/<int:pk>', ProfileView, name='profile'),
    path('order/<int:pk>', Order, name='order'),
    path('profile/edit/<int:pk>', ClientEditView.as_view(), name='profile_edit'),
    path('order/followers/add', AddFollowerView, name='add_follower'),
    path('order/followers/remove', RemoveFollowerView, name='remove_follower'),
    path('order/followers/staffremove/<int:pk>', RemoveFollowerStaffView, name='remove_follower_staff'),
    path('notification/<int:notification_pk>/profile/<int:profile_pk>', FollowNotification.as_view(), name='follow-notification'),
    path('notification/<int:notification_pk>/message/<int:message_pk>', MessageNotification.as_view(), name='message-notification'),
    path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_pk>/post/<int:post_pk>', CommentNotification.as_view(), name='comment-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),
    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/<int:pk>', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message', CreateMessage.as_view(), name='create-message'),
    path('user-search/', UserSearch.as_view(), name='user-search'),
    path('search/', TemplateView.as_view(template_name="user-search.html"), name='search'),
    path('order/', include('customer.urls')),
    path('dashboard/', include('dashboard.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
