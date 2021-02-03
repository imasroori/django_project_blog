from django.contrib import admin

from .models import Post, Comment, Label, Category, UserInfo, LabelPost, MyModel


# from django_summernote.admin import SummernoteModelAdmin
from .models import Post

admin.site.register(UserInfo)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(LabelPost)

admin.site.register(MyModel)


#
# class PostAdmin(SummernoteModelAdmin):
#     summernote_fields = ('content',)
#
# admin.site.register(Post, PostAdmin)

# @admin.register(Comment)
# class QuillPostAdmin(admin.ModelAdmin):
#     pass
