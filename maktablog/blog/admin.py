from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.checks import messages

from django.utils.safestring import mark_safe

from .models import Post, Comment, Label, Category, UserInfo, LabelPost


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    # show_change_link = True


class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("اطلاعات کاربری", {'fields': (
            'username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',)}),
        ("گروه کاربری و اجازه ها", {'fields': ('groups', 'user_permissions')}),

    )

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', ]
    inlines = [UserInfoInline]
    filter_horizontal = ['groups', 'user_permissions']


class LabelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('label_name',)}),

    )
    # inlines = [PostInline]
    list_display = ['label_name', 'count_posts']

    def count_posts(self, obj):
        return obj.post_set.count()

    count_posts.short_description = 'تعداد پست ها'

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('category_name', 'category')}),

    )
    # inlines = [PostInline]
    list_display = ['category_name', 'category', 'count_posts']

    def count_posts(self, obj):
        return obj.post_set.count()

    count_posts.short_description = 'تعداد پست ها'


class LabelPostInline(admin.TabularInline):
    model = LabelPost
    extra = 0


class PostInline(admin.TabularInline):
    model = Post


class CommentInline(admin.StackedInline):
    model = Comment


class CommentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'post')}),
        ("جزئیات نظر", {'fields': ('text', 'verificated', 'pub_date')}),
    )
    # inlines = [PostInline]
    list_display = ['user', 'return_title_post', 'verificated', 'get_link_post']
    readonly_fields = ['user', 'pub_date']

    def return_title_post(self, obj):
        return obj.post.title

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        if request.user.has_perm('blog.can_verify'):
            return True
        else:
            return False

    def make_verify_comment(self, request, queryset):
        if not request.user.has_perm('blog.can_verify'):
            return self.message_user(request, "شما دسترسی لازم را ندارید!", level=messages.ERROR)
        queryset.update(verificated=True)
        return self.message_user(request,
                                 "{} نظر با موفقیت تایید شد.".format(queryset.count()))

    def make_unverify_comment(self, request, queryset):
        if not request.user.has_perm('blog.can_unverify'):
            return self.message_user(request, "شما دسترسی لازم را ندارید!", level=messages.ERROR)
        queryset.update(verificated=False)
        return self.message_user(request,
                                 "{} نظر با موفقیت تایید شد.".format(queryset.count()))

    def get_link_post(self, obj):
        return mark_safe('<a class="btn" href="/%s/show_post">نمایش متن پست</a>' % obj.post.id)

    get_link_post.short_description = "مشاهده پست مربوطه"
    make_verify_comment.short_description = "تایید کردن نظرات انتخابی"
    make_unverify_comment.short_description = "رد کردن نظرات انتخابی"
    return_title_post.short_description = "عنوان پست"

    actions = [make_verify_comment, make_unverify_comment]


class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ("اطلاعات پست", {'fields': ('user', 'title', 'image', 'text')}),
        ("زمان و تاریخ", {'fields': ('created_at', 'updated_at')}),
        ("وضعیت", {'fields': ('activated', 'verificated')}),
        ("طبقه بندی و برچسب ها", {'fields': ('category',)}),
    )

    readonly_fields = ('created_at', 'updated_at')
    inlines = [LabelPostInline]

    def num_likes(self, obj):
        return obj.likes.count()

    def num_dislikes(self, obj):
        return obj.dislikes.count()

    def num_comments(self, obj):
        return obj.comment_set.count(), obj.comment_set.all().filter(verificated=True).count()

    num_likes.short_description = 'تعداد پسندیدن'
    num_dislikes.short_description = 'تعداد نپسندیدن'
    num_comments.short_description = 'کل نظرات/تایید شده'
    list_display = ['title', 'user', 'activated', 'verificated', 'num_likes', 'num_dislikes', 'num_comments',
                    'show_link_comments', ]
    list_display_links = ('title', 'show_link_comments',)

    # filter_horizontal = ['likes', 'dislikes', 'star']

    def show_link_comments(self, obj):
        return mark_safe('<a class="btn" href="/%s/show_post/#comments-post">نمایش نظرات</a>' % obj.id)

    show_link_comments.short_description = "مشاهده صفحه نظرات"

    def make_activate_post(self, request, queryset):
        queryset.update(activated=True)
        return self.message_user(request,
                                 "{} پست با موفقیت فعال شد.".format(queryset.count()))

    def make_deactivate_post(self, request, queryset):
        queryset.update(activated=False)
        return self.message_user(request,
                                 "{} پست با موفقیت غیرفعال شد.".format(queryset.count()))

    def make_verify_post(self, request, queryset):
        if not request.user.has_perm('blog.can_verify'):
            return self.message_user(request, "شما دسترسی لازم را ندارید!", level=messages.ERROR)
        queryset.update(verificated=True)
        return self.message_user(request,
                                 "{} پست با موفقیت تایید شد.".format(queryset.count()))

    def make_unverify_post(self, request, queryset):
        if not request.user.has_perm('blog.can_verify'):
            return self.message_user(request, "شما دسترسی لازم را ندارید!", level=messages.ERROR)
        queryset.update(verificated=False)
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
        if not request.user.has_perm('blog.can_verify'):
            form.base_fields['user'].initial = request.user
            disabled_fields = ('user', 'created_at', 'updated_at', 'verificated')

        if request.user.has_perm('blog.can_verify'):
            form.base_fields['user'].initial = request.user
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


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Category, CategoryAdmin)
