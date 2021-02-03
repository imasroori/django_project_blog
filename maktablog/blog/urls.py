from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    (path('', views.index, name='index')),
    (path('register', views.register, name='register')),
    (path('<int:id>/show_post', views.ShowPost.as_view(), name='show_post')),
    (path('show_all_posts', views.ShowAllPosts.as_view(), name='show_all_posts')),
    (path('<int:id>/profile', views.Profile.as_view(), name='profile')),
]
