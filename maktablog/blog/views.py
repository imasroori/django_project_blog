from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q, Count
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.shortcuts import render, redirect
from django.views import generic
from khayyam import JalaliDate
from persiantools import jdatetime
import random
from .forms import SignUpForm, UserUpdateForm, UserInfoUpdateForm
from .models import Post, Category, Label
from .views_functions import simple_search, advanced_search


class SearchPostView(generic.ListView):
    """
    With query to database in search-box, return results.
    Search in label,writer,text,title of posts in 2 methods: advanced and simple
    """
    template_name = 'blog/search.html'

    def get(self, request, *args, **kwargs):
        """
        This function design for handle GET method in queries for searching in database.
        """
        query = request.GET.get('query', None)
        if query:
            context = simple_search(query)
            return render(request, self.template_name, context)

        elif (request.GET.get('title', None) or request.GET.get('text', None) or
              request.GET.get('writer', None) or request.GET.get('label', None) or
              request.GET.get('date-start', None) or request.GET.get('date-end', None)):
            q_title = request.GET.get('title', None)
            q_text = request.GET.get('text', None)
            q_writer = request.GET.get('writer', None)
            q_label = request.GET.get('label', None)

            s_date = request.GET.get('date-start', None)
            e_date = request.GET.get('date-end', None)
            context = advanced_search(q_label=q_label, q_title=q_title, q_text=q_text, q_writer=q_writer, s_date=s_date,
                                      e_date=e_date)
            if context == 'error':
                messages.add_message(request, messages.WARNING, 'قالب تاریخ را به درستی وارد کنید!')
                return render(request, self.template_name, {'posts_advanced_search': [""]})
            return render(request, self.template_name, context)
        else:
            messages.add_message(request, messages.WARNING, 'لطفا در محل جستجو چیزی وارد کنید.')
            return render(request, self.template_name, {'posts_advanced_search': [""]})


class ShowAllCategories(generic.ListView):
    """
    Class-based view for rendering all categoreis in one page
    """
    template_name = 'blog/show_all_categories.html'
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()


class PostsinLabel(generic.DetailView):
    """
    Class-based view for rendering all posts in same labels(tags) in one page
    """
    pk_url_kwarg = 'id'
    template_name = 'blog/all_posts_in_label.html'
    model = Label
    context_object_name = 'post_in_label'

    def get_context_data(self, **kwargs):
        context = super(PostsinLabel, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostsinCategory(generic.DetailView):
    """
    Class-based view for rendering all posts in same categories in one page
    """
    pk_url_kwarg = 'id'
    template_name = 'blog/all_posts_in_category.html'
    model = Category
    context_object_name = 'post_in_category'

    def get_context_data(self, **kwargs):
        context = super(PostsinCategory, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class IndexView(generic.ListView):
    """
    Class-based view for show main page
    This class passed two parameters to template :=> posts and categories
    """
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        ids = [i.id for i in Post.objects.filter(activated=True, verificated=True)]
        random.shuffle(ids)
        shuffled = [Post.objects.get(id=i) for i in ids]
        query_set = shuffled[:6]
        return query_set

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ShowPost(generic.DetailView):
    """
    Class-based view for rendering one post contains all verified comments in one page
    """
    pk_url_kwarg = 'id'
    model = Post
    context_object_name = 'post_detail'
    template_name = 'blog/show_one_post.html'


class ShowAllPosts(generic.ListView):
    """
    Class-based view for rendering all posts in one page
    This class passed two parameters to template :=> posts and categories
    """
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().filter(activated=True, verificated=True)

    def get_context_data(self, **kwargs):
        context = super(ShowAllPosts, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@login_required
def profile(request):
    """
    Func-based view for visiting and updating personal information
    POST method :=> for updating and submit form
    GET method :=> for visiting form
    """
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
    """ Render popular posts that have maximum likes"""
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.annotate(like_count=Count('likes')).filter(activated=True).order_by('-like_count')[:20]

    def get_context_data(self, **kwargs):
        context = super(PopularPosts, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class NewestPosts(generic.ListView):
    """ Render newest posts that published recently"""
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')[:20]

    def get_context_data(self, **kwargs):
        context = super(NewestPosts, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


def signup(request):
    """
    func-based view for sign-up in site
    POST method :=> for submitting form in site
    GET method :=> for rendering form in template
    """
    if request.POST:
        signup_form = SignUpForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            userinfo = signup_form.save()

            user.refresh_from_db()
            userinfo.refresh_from_db()

            user.userinfo.alias_name = signup_form.cleaned_data.get('alias_name')
            user.userinfo.phone_number = signup_form.cleaned_data.get('phone_number')
            user.userinfo.image = signup_form.cleaned_data['image']

            user.first_name = signup_form.cleaned_data.get('first_name')
            user.last_name = signup_form.cleaned_data.get('last_name')
            user.email = signup_form.cleaned_data.get('email')

            userinfo.save()
            user.save()

            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            groups = Group.objects.all()
            for g in groups:
                if Permission.objects.get(name='Can add post') not in g.permissions.all():
                    simple_group = g
                    user.groups.add(simple_group.id)
                    break

            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'ثبت نام شما با موفقیت انجام شد، خوش آمدید')
            return redirect("/blog/")

        else:
            messages.add_message(request, messages.WARNING, 'خطا در ثبت نام')
            return render(request, 'blog/signup.html', {'signup_form': signup_form})

    else:
        signup_form = SignUpForm()
        return render(request, 'blog/signup.html', {'signup_form': signup_form})


class UserStaredPosts(generic.ListView):
    """
    Class-based view for show all stared posts for each user
    """
    template_name = 'blog/user_stared_posts.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        qs = Post.objects.all()
        stared_posts = []
        for post in qs:
            if user not in post.star.all():
                continue
            stared_posts.append(post)
        # stared_posts = qs
        context = {
            'stared_posts': stared_posts,
        }
        return render(request, self.template_name, context)


class AboutUsView(generic.ListView):
    """
    Class-based view for rendering About-Us page
    """
    template_name = 'blog/about_us.html'
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()


class Roles(generic.ListView):
    """
    Class-based view for rendering Roles page
    """
    template_name = 'blog/roles.html'
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()
