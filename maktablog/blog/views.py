from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Post, MyModel, UserInfo, Category, Label


# def index(request):
#     return render(request, 'blog/index.html')


class ShowAllCategories(generic.ListView):
    template_name = 'blog/show_all_categories.html'
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()


class PostsinLabel(generic.DetailView):
    pk_url_kwarg = 'id'
    template_name = 'blog/all_posts_in_label.html'
    model = Label
    context_object_name = 'post_in_label'

    def get_context_data(self, **kwargs):
        context = super(PostsinLabel, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostsinCategory(generic.DetailView):
    pk_url_kwarg = 'id'
    template_name = 'blog/all_posts_in_category.html'
    model = Category
    context_object_name = 'post_in_category'

    def get_context_data(self, **kwargs):
        context = super(PostsinCategory, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


def register(request):
    if request.POST:
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        alias_name = request.POST['alias_name']
        user_name = request.POST['username']
        pass_word = request.POST['password']
        phone = request.POST['phone_number']
        img = request.POST.get('image_profile')
        print("dfdfdfdfdf", img)
        user = User.objects.create_user(password=pass_word, username=user_name, first_name=f_name, last_name=l_name)

        user.is_staff = True
        userinfo = UserInfo.objects.create(user=user, phone_number=phone, alias_name=alias_name, image="images/" + img)
        userinfo.save()
        print(user.userinfo.image)
        user.save()
    return HttpResponse(render(request, 'blog/register_form.html'))


class ShowPost(generic.DetailView):
    pk_url_kwarg = 'id'
    model = Post
    context_object_name = 'post_detail'
    template_name = 'blog/show_one_post.html'


# class CategoryPost(generic.DetailView):
#     pk_url_kwarg = 'id'
#     template_name = 'blog/all_posts_in_category.html'
#     model = Category
#     context_object_name = 'post_in_category'
#
#     def get_context_data(self, **kwargs):
#         context = super(CategoryPost, self).get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         return context


class ShowAllPosts(generic.ListView):
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ShowAllPosts, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class Profile(LoginRequiredMixin, generic.DetailView):
    # login_url = '/login/'

    model = User
    pk_url_kwarg = 'id'
    context_object_name = 'user_profile'
    template_name = 'blog/profile.html'


class PopularPosts(generic.ListView):
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().filter(title__contains='پایتون')


class NewestPosts(generic.ListView):
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().filter(title__contains='برف')
