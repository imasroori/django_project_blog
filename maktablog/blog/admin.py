from django.contrib import admin

from .models import Post, Comment, Label, Category, UserInfo, LabelPost

admin.site.register(UserInfo)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(LabelPost)
