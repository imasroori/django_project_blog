from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    (path('validate_username', views.validate_username, name='validate_username')),
    (path('dislike_post', views.dislike_post, name='dislike_post')),
    (path('like_post', views.like_post, name='like_post')),
    (path('star_post', views.star_post, name='star_post')),
    (path('comment_post_form', views.comment_post_form, name='comment_post_form')),
    (path('like_comment', views.like_comment, name='like_comment')),
    (path('dislike_comment', views.dislike_comment, name='dislike_comment')),
]
