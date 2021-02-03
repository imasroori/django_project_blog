from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Post, MyModel, UserInfo


def index(request):
    return render(request, 'blog/index.html')


def register(request):
    if request.POST:
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        alias_name = request.POST['alias_name']
        user_name = request.POST['username']
        pass_word = request.POST['password']
        phone = request.POST['phone_number']
        img = request.POST['image_profile']
        user = User.objects.create_user(password=pass_word, username=user_name, first_name=f_name, last_name=l_name)
        user.is_staff = True
        userinfo = UserInfo.objects.create(user=user, phone_number=phone, alias_name=alias_name, image=img)
        userinfo.save()
        user.save()
    return HttpResponse(render(request, 'blog/register_form.html'))


class ShowPost(generic.DetailView):
    pk_url_kwarg = 'id'
    model = Post
    context_object_name = 'post_detail'
    template_name = 'blog/show_post.html'


class ShowAllPosts(generic.ListView):
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()


class Profile(generic.DetailView):
    model = User
    pk_url_kwarg = 'id'
    context_object_name = 'user_profile'
    template_name = 'blog/profile.html'
