from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from blog.models import *

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from blog.serializers import CommentSerializer, LikePostSerializer, DisLikePostSerializer, StarPost, \
    DisLikeCommentSerializer, LikeCommentSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class AutoCompleteSearch(APIView):

    def get(self, request):
        query = request.GET.get('query', None)
        if query:
            print(query)
            qs = Post.objects.all().filter(
                Q(title__startswith=query) | Q(text__startswith=query) | Q(
                    labelpost__label_name__startswith=query) | Q(
                    user__username__startswith=query)).distinct()

            serializer = PostSerializer(qs, many=True)
            print(serializer)
            print(serializer.data)
            return Response(serializer.data)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


@api_view(['GET'])
def like_post(request):
    user = User.objects.get(username=request.user)
    post = Post.objects.get(id=request.GET.get('post_id'))
    param = {
        # 'user': user.id,
        'post': post.id,

    }

    print(request.GET.get('post_id'))
    serializer = LikePostSerializer(post, data=param)
    # print(request.data)

    if serializer.is_valid():
        result = serializer.save(user_id=request.user.id)
        print("serializer", result)

        return Response(result)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def dislike_post(request):
    user = User.objects.get(username=request.user)
    post = Post.objects.get(id=request.GET.get('post_id'))

    param = {
        'post': post.id,
    }
    serializer = DisLikePostSerializer(post, data=param)

    if serializer.is_valid():
        result = serializer.save(user_id=request.user.id)
        print("serializer", result)

        return Response(result)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def star_post(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        post = Post.objects.get(id=request.GET.get('post_id'))
        param = {
            'user': user.id,
            'post': post.id,

        }

        serializer = StarPost(post, data=param)

        if serializer.is_valid():
            # print(serializer.data)
            result = serializer.save(user_id=request.user.id)
            # print('serializer', serializer.data)
            # print(result)
            # print(serializer.data)
            return Response(result)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def comment_post_form(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        user = User.objects.get(username=request.user)
        print(request.data)
        param = {
            'user': user.pk,
            'post': int(request.data['post']),
            'text': request.data['text'],
        }

        serializer = CommentSerializer(data=param)

        if serializer.is_valid():
            # print(serializer.data)
            serializer.save()
            print(serializer)
            # print(serializer.data)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def like_comment(request):
    user = User.objects.get(username=request.user)
    # post = Post.objects.get(id=request.GET.get('post_id'))
    comment = Comment.objects.get(id=request.GET.get('comment_id'))
    param = {
        # 'user': user.id,
        # 'post': post.id,
        'comment': comment.id,

    }

    # print(request.GET.get('post_id'))
    serializer = LikeCommentSerializer(comment, data=param)
    # print(request.data)

    if serializer.is_valid():
        result = serializer.save(user_id=request.user.id)
        print("serializer", result)

        return Response(result)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def dislike_comment(request):
    user = User.objects.get(username=request.user)
    # post = Post.objects.get(id=request.GET.get('post_id'))
    comment = Comment.objects.get(id=request.GET.get('comment_id'))

    param = {
        # 'post': post.id,
        'comment': comment.id,
    }
    serializer = DisLikeCommentSerializer(comment, data=param)

    if serializer.is_valid():
        result = serializer.save(user_id=request.user.id)
        print("serializer", result)

        return Response(result)
    return Response(serializer.errors, status=400)
