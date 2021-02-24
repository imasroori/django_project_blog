from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    """Serializer post for use in auto-complete search box"""

    class Meta:
        model = Post
        fields = ['title', 'text', 'label_post_set', 'user']


class StarPost(serializers.ModelSerializer):
    """Serializer post for use in staring post and saved it"""

    class Meta:
        model = Post
        fields = ['star']

    def update(self, instance, validated_data):
        """
        checking user stared this post or not,
        Toggle star-icon in template and updating state in server
        """
        post = instance

        a = False
        if validated_data['user_id'] in self.data[
            'star']:  # user.id that passed to serializer from API view is available in validated_data
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
    """Serializer post for use in like-post"""

    class Meta:
        model = Post
        fields = ['likes']

    def update(self, instance, validated_data):
        """
        checking user liked this post or not,
        Toggle like-icon in template and updating state in server
        Check if user disliked this post,  must be dislike-icon disabled
        """
        post = instance
        print("val", validated_data['user_id'])
        a = b = False
        user = User.objects.get(
            id=validated_data['user_id'])  # user.id that passed to serializer is available in validated_data
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
    """Serializer post for use in dislike-post"""

    class Meta:
        model = Post
        fields = ['dislikes']

    def update(self, instance, validated_data):
        """
        checking user disliked this post or not,
        Toggle dislike-icon in template and updating state in server
        Check if user liked this post,  must be like-icon disabled
        """
        post = instance
        a = b = False
        user = User.objects.get(
            id=validated_data['user_id'])  # user.id that passed to serializer is available in validated_data
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
    """Serializer comment for submit comment users on bottom posts"""

    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'user']


class LikeCommentSerializer(serializers.ModelSerializer):
    """Serializer Comment for check user liked this comment or not"""

    class Meta:
        model = Comment
        fields = ['likes']

    def update(self, instance, validated_data):
        """
        checking user liked this comment or not,
        Toggle like-icon in template and updating state in server
        Check if user disliked this comment,  must be dislike-icon disabled
        """
        comment = instance
        print("val", validated_data['user_id'])
        a = b = False
        user = User.objects.get(
            id=validated_data['user_id'])  # user.id that passed to serializer is available in validated_data
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
        """
        checking user disliked this comment or not,
        Toggle dislike-icon in template and updating state in server
        Check if user liked this comment,  must be like-icon disabled
        """
        comment = instance
        a = b = False
        user = User.objects.get(
            id=validated_data['user_id'])  # user.id that passed to serializer is available in validated_data
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
