from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.mail import message

from .models import Post, Comment, Label, Category, UserInfo, LabelPost, MyModel


# class LabelPostAdmin(admin.TabularInline):
#     list_display = ['label']


class LabelPostInline(admin.TabularInline):
    model = LabelPost


class PostInline(admin.TabularInline):
    model = Post


class CommentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'post')}),
        ("جزئیات نظر", {'fields': ('text', 'verification', 'date')}),
    )
    # inlines = [PostInline]
    readonly_fields = ['user']


class CommentInline(admin.StackedInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ("اطلاعات پست", {'fields': ('user', 'title', 'image', 'text',)}),
        # ("زمان و تاریخ", {'fields': ('created_at',)}),
        ("وضعیت", {'fields': ('activation', 'verification')}),
        ("طبقه بندی و برچسب ها", {'fields': ('category',)}),
    )

    # readonly_fields = ('user', 'created_at', 'updated_at', 'verification')
    inlines = [LabelPostInline]
    list_display = ['title', 'user', 'activation', 'verification']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()
        if request.user.has_perm('blog.add_post'):
            disabled_fields = ('user', 'created_at', 'updated_at', 'verification')
        for item in disabled_fields:
            if item in form.base_fields:
                form.base_fields[item].disabled = True

        return form

    def get_queryset(self, request):
        if request.user.has_perm('blog.add_post'):
            qs = super(PostAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)
        else:
            qs = super(PostAdmin, self).get_queryset(request)
            return qs

    # def get_form(self):
    #     pass

    def make_activate_post(self, request, queryset):
        queryset.update(activation=True)
        return self.message_user(request,
                                 "{} پست با موفقیت فعال شد.".format(queryset.count()))

    def make_deactivate_post(self, request, queryset):
        queryset.update(activation=False)
        return self.message_user(request,
                                 "{} پست با موفقیت غیرفعال شد.".format(queryset.count()))

    def make_verify_post(self, request, queryset):
        queryset.update(verification=True)
        return self.message_user(request,
                                 "{} پست با موفقیت تایید شد.".format(queryset.count()))

    def make_unverify_post(self, request, queryset):
        queryset.update(verification=False)
        return self.message_user(request,
                                 "{} پست با موفقیت رد شد.".format(queryset.count()))

    make_activate_post.short_description = "فعال کردن پست های انتخابی"
    make_deactivate_post.short_description = "غیرفعال کردن پست های انتخابی"
    make_verify_post.short_description = "تایید کردن پست های انتخابی"
    make_unverify_post.short_description = "رد کردن پست های انتخابی"

    actions = [make_activate_post, make_deactivate_post, make_verify_post, make_unverify_post]


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
