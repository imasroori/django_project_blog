from django.contrib import admin
from django.contrib.auth.models import User

from .models import Post, Comment, Label, Category, UserInfo, LabelPost, MyModel


class LabelPostInline(admin.TabularInline):
    model = LabelPost


class PostInline(admin.TabularInline):
    model = Post


class CommentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('post',)}),
        ("جزئیات نظر", {'fields': ('text', 'verification', 'date')}),
    )
    # inlines = [PostInline]


class CommentInline(admin.StackedInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ("اطلاعات پست", {'fields': ('user','title', 'image', 'text',)}),
        # ("زمان و تاریخ", {'fields': ('pub_date',)}),
        ("وضعیت", {'fields': ('activation', 'verification')}),
        ("طبقه بندی و برچسب ها", {'fields': ('category',)}),
    )
    inlines = [LabelPostInline]


admin.site.register(UserInfo)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
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
