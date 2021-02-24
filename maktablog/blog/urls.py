from django.urls import path

from . import views

app_name = 'blog'  # For use in template tags :=> {% url 'app_name:view_name' %}
# Routing all pages and requests in blog APP with urlpatterns
urlpatterns = [
    (path('', views.IndexView.as_view(), name='index')),
    (path('signup', views.signup, name='signup')),
    (path('<int:id>/show_post', views.ShowPost.as_view(), name='show_post')),
    (path('<int:id>/show_post/', views.ShowPost.as_view(), name='show_post')),
    (path('show_all_posts', views.ShowAllPosts.as_view(), name='show_all_posts')),
    (path('profile', views.profile, name='profile')),
    (path('<int:id>/posts_in_category', views.PostsinCategory.as_view(), name='posts_in_category')),
    (path('<int:id>/posts_in_label', views.PostsinLabel.as_view(), name='posts_in_label')),
    (path('show_all_categories', views.ShowAllCategories.as_view(), name='show_all_categories')),
    (path('popular_posts', views.PopularPosts.as_view(), name='popular_posts')),
    (path('user_stared_posts', views.UserStaredPosts.as_view(), name='user_stared_posts')),
    (path('newest_posts', views.NewestPosts.as_view(), name='newest_posts')),
    (path('search', views.SearchPostView.as_view(), name='search')),

]
