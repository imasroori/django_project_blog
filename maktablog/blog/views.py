from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import generic
from .forms import SignUpForm, UserUpdateForm, UserInfoUpdateForm
from .models import Post, Category, Label


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
            print(query)
            qs = Post.objects.all().filter(
                Q(title__regex=r'^.*{}.*'.format(query)) | Q(text__regex=r'^.*{}.*'.format(query)) | Q(
                    labelpost__label_name__regex=r'^.*{}.*'.format(query)) | Q(
                    user__username__regex=r'^.*{}.*'.format(query))).distinct()
            context = {
                'posts': qs,
            }
            return render(request, self.template_name, context)
        else:
            q_title = request.GET.get('title', None)
            q_text = request.GET.get('text', None)
            q_writer = request.GET.get('writer', None)
            q_label = request.GET.get('label', None)
            # q_label=request.GET.get('label',None)
            qs = Post.objects.all().filter(
                Q(title__icontains=q_title) & Q(text__icontains=q_text) & Q(
                    labelpost__label_name__icontains=q_label) & Q(
                    user__username__icontains=q_writer)).distinct()
            context = {
                'posts': qs,
            }
            return render(request, self.template_name, context)


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
        return Post.objects.all().filter(activated=True, verificated=True)

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
        return Post.objects.all().filter(activated=True)


class NewestPosts(generic.ListView):
    """ Render newest posts that published recently"""
    template_name = 'blog/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all().filter(title__contains='برف')

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
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'شما با موفقیت ثبت نام کردید، خوش آمدید')
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
        stared_posts = Post.objects.filter(star=True)
        context = {
            'stared_posts': stared_posts,
        }
        return render(request, self.template_name, context)
