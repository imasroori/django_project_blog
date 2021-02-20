from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment


class StarPost(serializers.ModelSerializer):
    # star =
    class Meta:
        model = Post
        fields = ['star']

    def update(self, instance, validated_data):
        post = instance

        a = False
        if validated_data['user_id'] in self.data['star']:
            a = True
            post.star.remove(validated_data['user_id'])
        else:
            a = False
            post.star.add(validated_data['user_id'])

        data = {
            'is_stared': a,
        }
        instance.save()
        return data


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['likes']

    def update(self, instance, validated_data):
        post = instance
        print("val", validated_data['user_id'])
        a = b = False
        user = User.objects.get(id=validated_data['user_id'])
        if user in post.likes.all():
            a = True
            post.likes.remove(user)
        else:
            if user in post.dislikes.all():
                b = True
                post.dislikes.remove(user)
            a = False
            post.likes.add(user)
        data = {
            'is_liked': a,
            'is_in_disliked': b,

        }
        instance.save()
        return data


class DisLikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['dislikes']

    def update(self, instance, validated_data):
        post = instance
        a = b = False
        user = User.objects.get(id=validated_data['user_id'])
        if user in post.dislikes.all():
            a = True
            post.dislikes.remove(user)
        else:
            if user in post.likes.all():
                b = True
                post.likes.remove(user)
            a = False
            post.dislikes.add(user)
        data = {
            'is_disliked': a,
            'is_in_liked': b,

        }
        instance.save()
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'user']


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['likes']

    def update(self, instance, validated_data):
        comment = instance
        print("val", validated_data['user_id'])
        a = b = False
        user = User.objects.get(id=validated_data['user_id'])
        if user in comment.likes.all():
            a = True
            comment.likes.remove(user)
        else:
            if user in comment.dislikes.all():
                b = True
                comment.dislikes.remove(user)
            a = False
            comment.likes.add(user)
        data = {
            'is_liked': a,
            'is_in_disliked': b,

        }
        instance.save()
        return data


class DisLikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['dislikes']

    def update(self, instance, validated_data):
        comment = instance
        a = b = False
        user = User.objects.get(id=validated_data['user_id'])
        if user in comment.dislikes.all():
            a = True
            comment.dislikes.remove(user)
        else:
            if user in comment.likes.all():
                b = True
                comment.likes.remove(user)
            a = False
            comment.dislikes.add(user)
        data = {
            'is_disliked': a,
            'is_in_liked': b,

        }
        instance.save()
        return data
