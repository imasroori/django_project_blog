from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.checks import messages
from django.core.mail import message

from .models import Post, Comment, Label, Category, UserInfo, LabelPost, MyModel


# class LabelPostAdmin(admin.TabularInline):
#     list_display = ['label']


class LabelPostInline(admin.TabularInline):
    model = LabelPost
    extra = 0


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

    def num_likes(self, obj):
        return 2

    def num_dislikes(self, obj):
        return 2

    def num_comments(self, obj):
        return 1

    num_likes.short_description = 'تعداد پسندیدن'
    num_dislikes.short_description = 'تعداد نپسندیدن'
    num_comments.short_description = 'تعداد نظرات'
    list_display = ['title', 'user', 'activation', 'verification', 'num_likes', 'num_dislikes', 'num_comments']

    def make_activate_post(self, request, queryset):
        queryset.update(activation=True)
        return self.message_user(request,
                                 "{} پست با موفقیت فعال شد.".format(queryset.count()))

    def make_deactivate_post(self, request, queryset):
        queryset.update(activation=False)
        return self.message_user(request,
                                 "{} پست با موفقیت غیرفعال شد.".format(queryset.count()))

    def make_verify_post(self, request, queryset):
        if not request.user.has_perm('blog.can_verify'):
            return self.message_user(request, "شما دسترسی لازم را ندارید!", level=messages.ERROR)
        queryset.update(verification=True)
        return self.message_user(request,
                                 "{} پست با موفقیت تایید شد.".format(queryset.count()))

    def make_unverify_post(self, request, queryset):
        if not request.user.has_perm('blog.can_verify'):
            return self.message_user(request, "شما دسترسی لازم را ندارید!", level=messages.ERROR)
        queryset.update(verification=False)
        return self.message_user(request,
                                 "{} پست با موفقیت رد شد.".format(queryset.count()))

    make_activate_post.short_description = "فعال کردن پست های انتخابی"
    make_deactivate_post.short_description = "غیرفعال کردن پست های انتخابی"
    make_verify_post.short_description = "تایید کردن پست های انتخابی"
    make_unverify_post.short_description = "رد کردن پست های انتخابی"
    actions = [make_activate_post, make_deactivate_post, make_verify_post, make_unverify_post]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()
        if request.user.has_perm('blog.add_post') and not request.user.is_superuser:
            form.base_fields['user'].initial = request.user
            disabled_fields = ('user', 'created_at', 'updated_at', 'verification')

        if request.user.has_perm('blog.change_post') and not request.user.has_perm('blog.add_post'):
            disabled_fields = ('user', 'created_at', 'updated_at')
        for item in disabled_fields:
            if item in form.base_fields:
                form.base_fields[item].disabled = True
        return form

    def get_queryset(self, request):
        if request.user.has_perm('blog.can_verify'):
            qs = super(PostAdmin, self).get_queryset(request)
            return qs
        elif not request.user.has_perm('blog.can_verify'):
            qs = super(PostAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('blog.can_verify'):
            if 'make_verify_post' in actions:
                del actions['make_verify_post']
            if 'make_unverify_post' in actions:
                del actions['make_unverify_post']
        return actions


admin.site.register(UserInfo)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Label)
admin.site.register(Category)
admin.site.register(LabelPost)

admin.site.register(MyModel)
