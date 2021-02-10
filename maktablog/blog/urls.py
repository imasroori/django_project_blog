from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    (path('', views.IndexView.as_view(), name='index')),
    (path('register', views.register, name='register')),
    (path('<int:id>/show_post', views.ShowPost.as_view(), name='show_post')),
    (path('show_all_posts', views.ShowAllPosts.as_view(), name='show_all_posts')),
    (path('<int:id>/profile', views.Profile.as_view(), name='profile')),
    (path('<int:id>/post_category', views.CategoryPost.as_view(), name='post_category')),
    (path('<int:id>/posts_in_category', views.PostsinCategory.as_view(), name='posts_in_category')),
    (path('show_all_categories', views.ShowAllCategories.as_view(), name='show_all_categories')),

]
