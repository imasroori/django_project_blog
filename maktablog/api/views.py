from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse

from blog.models import *

from rest_framework.decorators import api_view

from blog.serializers import CommentSerializer, LikePostSerializer, DisLikePostSerializer, StarPost, \
    DisLikeCommentSerializer, LikeCommentSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class AutoCompleteSearch(APIView):
    """
    API for autocomplete search
    This is incomplete ==> Ignore this API
    """

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
    """
    Check username there are in database or not, if username there are in database raise error
    """
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


@api_view(['GET'])
def like_post(request):
    """
    With GET method ajax get post.id and checking in serializer to toggle it
    """
    post = Post.objects.get(id=request.GET.get('post_id'))
    param = {
        'post': post.id,

    }
    serializer = LikePostSerializer(post, data=param)
    if serializer.is_valid():
        result = serializer.save(user_id=request.user.id)  # pass user.id to serializer,available in validated_data
        return Response(result)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def dislike_post(request):
    """
    With GET method ajax get post.id and checking in serializer to toggle it
    """
    post = Post.objects.get(id=request.GET.get('post_id'))

    param = {
        'post': post.id,
    }
    serializer = DisLikePostSerializer(post, data=param)

    if serializer.is_valid():
        result = serializer.save(user_id=request.user.id)  # pass user.id to serializer,available in validated_data

        return Response(result)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def star_post(request):
    """
    With GET method ajax get post.id and user.id to star post for loggined user [toggle star-icon]
    """
    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        post = Post.objects.get(id=request.GET.get('post_id'))
        param = {
            'user': user.id,
            'post': post.id,
        }

        serializer = StarPost(post, data=param)

        if serializer.is_valid():
            result = serializer.save(user_id=request.user.id)  # pass user.id to serializer,available in validated_data
            return Response(result)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def comment_post_form(request):
    """
    With POST method comment form submit. In this view the recieved data updated and pass to serializer
    """
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
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def like_comment(request):
    """
    Similar to like-post, in this view the comment.id available in GET method and toggle like icon
    """
    comment = Comment.objects.get(id=request.GET.get('comment_id'))
    param = {
        'comment': comment.id,
    }
    serializer = LikeCommentSerializer(comment, data=param)
    if serializer.is_valid():
        result = serializer.save(
            user_id=request.user.id)  # user.id passed to serializer and available in validated_data
        return Response(result)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def dislike_comment(request):
    """
    with pass comment.id to serializer check that this comment disliked or not,
    in update method on serializer checked to be like-icon off
    """
    comment = Comment.objects.get(id=request.GET.get('comment_id'))

    param = {
        'comment': comment.id,
    }
    serializer = DisLikeCommentSerializer(comment, data=param)

    if serializer.is_valid():
        result = serializer.save(user_id=request.user.id)

        return Response(result)
    return Response(serializer.errors, status=400)
