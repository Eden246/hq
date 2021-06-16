from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic import ListView
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib import messages

def Home(request):
        return render(request, 'home.html')

def SignupView(request):
    userform=UserForm()
    clientform=ClientForm()
    context={'userform':userform,'clientform':clientform}
    if request.method=='POST':
        userform=UserForm(request.POST)
        clientform=ClientForm(request.POST,request.FILES)
        if userform.is_valid() and clientform.is_valid():
            user=userform.save()
            password = user.password
            user.set_password(password)
            user.save()
            client=clientform.save(commit=False)
            client.user=user
            client.save()
            client_group = Group.objects.get_or_create(name='client')
            client_group[0].user_set.add(user)
        return redirect('home')
    return render(request,'signup.html',context=context)
    
class PostView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-date')
        form = PostForm()

        context = {
            'posts': posts,
            'form': form,
        }

        return render(request, 'post.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-date')
        form = PostForm(request.POST ,request.FILES)
        files = request.FILES.getlist("image")

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.client = request.user.client
            post.save()

            for f in files:
                img = Image(image=f)
                img.save()
                post.image.add(img)
            post.save()

        context = {
            'posts': posts,
            'form': form,
        }

        return render(request, 'post.html', context)

def post_json(request):
    data = list(Post.objects.values())
    return JsonResponse(data, safe=False)

class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-date')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

        comments = Comment.objects.filter(post=post).order_by('-date')

        notification = Notification.objects.create(notification_type=2, from_user=comment.user, to_user=post.user, comment=comment)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request,'post_detail.html',context=context)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields =['body']
    template_name = 'post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={'pk':pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user or self.request.user.is_staff or self.request.user.is_superuser

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs={'pk':pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user or self.request.user.is_staff or self.request.user.is_superuser

def ProfileView(request, pk):
        client = Client.objects.get(pk=pk)
        user = client.user
        posts = Post.objects.filter(user=user).order_by('-date')

        followers = client.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following =True
                break
            else:
                is_following = False

        number_of_followers = len(followers)


        context = {
            'user':user,
            'client':client,
            'posts':posts,
            'followers':followers,
            'number_of_followers':number_of_followers,
            'is_following':is_following,
            }
        return render(request, 'profile.html', context)

class ClientEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['phone', 'facility']
    template_name = 'client_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk':pk})

    def test_func(self):
        client = self.get_object()
        return self.request.user == client.user or self.request.user.is_staff or self.request.user.is_superuser

class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post_detail', pk=post_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')

class ListThreads(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request,*args, **kwargs):
        form = ThreadForm()
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        context = {'threads': threads,'form': form}
        return render(request, 'inbox.html', context)
        
    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)
            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver,
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('inbox')

class ThreadView(View):
    def get(self, request,pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context ={
            'thread':thread,
            'form':form,
            'message_list':message_list,
        }
        return render(request, 'thread.html', context)

class CreateMessage(View):
    def post(self, request,pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
        
        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )
        message.save()
        notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=message.receiver_user, message=message)

        return redirect('thread', pk=pk)

class MessageNotification(View):
    def get(self, request, notification_pk, message_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        message = MessageModel.objects.get(pk=message_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=message_pk)


class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk,*args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.parent = parent_comment
            comment.save()
        
        notification = Notification.objects.create(notification_type=2, from_user=comment.user, to_user=parent_comment.user, comment=comment)

        return redirect('post_detail', pk=post_pk)

class CommentNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post_detail', pk=post_pk)