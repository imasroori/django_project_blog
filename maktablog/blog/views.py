from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import generic

from .forms import SignUpForm, UserUpdateForm, UserInfoUpdateForm
from .models import Post, MyModel, UserInfo, Category, Label, Comment


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


def showpost(request, id):
    # post_detail = Post.objects.get(id=id)

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        post_id = id
        comment_text = request.POST['comment_body']
        post = Post.objects.all().filter(id=post_id)[0]
        # print(post)
        print(comment_text)
        print(post_id)
        print(user)

        comment = Comment.objects.create(user=user, post=post, text=comment_text)

        post_detail = Post.objects.get(id=id)
        return render(request, 'blog/show_one_post.html', {'post_detail': post_detail})
    post_detail = Post.objects.get(id=id)
    return render(request, 'blog/show_one_post.html', {'post_detail': post_detail})


# class ShowPost(generic.DetailView):
#     pk_url_kwarg = 'id'
#     model = Post
#     context_object_name = 'post_detail'
#     template_name = 'blog/show_one_post.html'
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


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


@login_required
def profile(request):
    if request.method == 'POST':
        userinfo_form = UserInfoUpdateForm(request.POST, request.FILES, instance=request.user.userinfo)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if userinfo_form.is_valid() and user_form.is_valid():
            user_form.save()
            userinfo_form.save()
            messages.success(request, 'اطلاعات حساب کاربری شما با موفقیت بروزرسانی شد')
            return redirect('/blog/profile')
    else:
        userinfo_form = UserInfoUpdateForm(instance=request.user.userinfo)
        user_form = UserUpdateForm(instance=request.user)

    context = {'userinfo_form': userinfo_form, 'user_form': user_form}
    return render(request, 'blog/profile.html', context)


class PopularPosts(generic.ListView):
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().filter(activation=True)


class NewestPosts(generic.ListView):
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().filter(title__contains='برف')


def signup(request):
    if request.POST:
        signup_form = SignUpForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            userinfo = signup_form.save()

            user.refresh_from_db()
            userinfo.refresh_from_db()

            # user.userinfo.first_name = signup_form.cleaned_data.get('first_name')
            # user.userinfo.last_name = signup_form.cleaned_data.get('last_name')
            user.userinfo.alias_name = signup_form.cleaned_data.get('alias_name')
            user.userinfo.phone_number = signup_form.cleaned_data.get('phone_number')
            user.userinfo.image = signup_form.cleaned_data['image']

            user.first_name = signup_form.cleaned_data.get('first_name')
            user.last_name = signup_form.cleaned_data.get('last_name')
            user.email = signup_form.cleaned_data.get('email')

            # user.userinfo.email = signup_form.cleaned_data.get('email')
            userinfo.save()
            user.save()

            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'شما با موفقیت ثبت نام کردید، خوش آمدید')
            return redirect("/blog/")

        else:
            messages.add_message(request, messages.WARNING, 'خطا در ثبت نام')
            return render(request, 'blog/signup.html', {'signup_form': signup_form})

    else:
        signup_form = SignUpForm()
        return render(request, 'blog/signup.html', {'signup_form': signup_form})
