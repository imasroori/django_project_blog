from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from blog.models import *
from django.views.decorators.csrf import csrf_exempt


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def like_dislike_post(request):
    user = User.objects.get(username=request.user)
    post_id = request.GET.get('post_id', None)
    like_dislike_id = request.GET.get('like_dislike', None)
    a = b = False
    if like_dislike_id == 'like':
        for ii in Post.objects.all().filter(id=post_id):
            if user in ii.likes.all():
                a = True
                ii.likes.remove(user)
            else:
                if user in ii.dislikes.all():
                    b = True
                    ii.dislikes.remove(user)
                a = False
                ii.likes.add(user)

        data = {
            'is_liked': a,
            'is_in_disliked': b,
        }
        return JsonResponse(data)
    if like_dislike_id == 'dislike':
        for ii in Post.objects.all().filter(id=post_id):
            if user in ii.dislikes.all():
                a = True
                ii.dislikes.remove(user)
            else:
                if user in ii.likes.all():
                    b = True
                    ii.likes.remove(user)
                a = False
                ii.dislikes.add(user)

        data = {
            'is_disliked': a,
            'is_in_liked': b,
        }
        return JsonResponse(data)


def star_post(request):
    user = User.objects.get(username=request.user)
    post_id = request.GET.get('post_id', None)
    # post = Post.objects.get(id=post_id)
    a = False
    for ii in Post.objects.all().filter(id=post_id):
        if user in ii.star.all():
            a = True
            ii.star.remove(user)
        else:
            a = False
            ii.star.add(user)

    data = {
        'is_stared': a,
    }
    return JsonResponse(data)
