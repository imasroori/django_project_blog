from django.urls import path

from . import views

app_name = 'ajax'
urlpatterns = [

    (path('validate_username', views.validate_username, name='validate_username')),
    (path('like_dislike_post', views.like_dislike_post, name='like_dislike_post')),
    (path('star_post', views.star_post, name='star_post')),
    # (path('ajax/dislike_post', views.dislike_post, name='dislike_post')),
]
