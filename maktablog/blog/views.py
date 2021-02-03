from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Post, MyModel


def index(request):
    return render(request, 'blog/index.html')


def register(request):
    if request.POST:
        pass
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
