from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    (path('', views.IndexView.as_view(), name='index')),
    (path('signup', views.signup, name='signup')),
    (path('<int:id>/show_post', views.showpost, name='show_post')),
    (path('show_all_posts', views.ShowAllPosts.as_view(), name='show_all_posts')),
    (path('profile', views.profile, name='profile')),
    (path('<int:id>/posts_in_category', views.PostsinCategory.as_view(), name='posts_in_category')),
    (path('<int:id>/posts_in_label', views.PostsinLabel.as_view(), name='posts_in_label')),
    (path('show_all_categories', views.ShowAllCategories.as_view(), name='show_all_categories')),
    (path('popular_posts', views.PopularPosts.as_view(), name='popular_posts')),
    (path('newest_posts', views.NewestPosts.as_view(), name='newest_posts')),

]
