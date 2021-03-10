from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserInfo(models.Model):
    alias_name = models.CharField('نام مستعار', max_length=30)
    phone_number = models.CharField('شماره تلفن', max_length=11)
    image = models.ImageField('عکس پروفایل', upload_to='images/', default='default/default-avatar.jpg')
    user = models.OneToOneField(User, verbose_name='کاربر', on_delete=models.CASCADE)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        verbose_name_plural = "پروفایل کاربران"


@receiver(post_save, sender=User)
def update_userinfo_signal(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)
    instance.userinfo.save()


class Text(models.Model):
    text = models.TextField("متن")
    likes = models.ManyToManyField(User,
                                   related_name='%(app_label)s_liked_%(class)ss',
                                   related_query_name='%(app_label)s_liked_%(class)ss', null=True, blank=True)
    dislikes = models.ManyToManyField(User,
                                      related_name='%(app_label)s_disliked_%(class)ss',
                                      related_query_name='%(app_label)s_disliked_%(class)ss', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE, related_name='%(class)s')

    class Meta:
        abstract = True


class Category(models.Model):
    category_name = models.CharField('نام دسته بندی', max_length=30)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='زیرمجموعه',
                                 related_name='category_sub', null=True,
                                 blank=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "دسته بندی ها"


class Label(models.Model):
    label_name = models.CharField('برچسب', max_length=30)

    def __str__(self):
        return self.label_name

    class Meta:
        verbose_name_plural = "برچسب ها"


class Post(Text):
    title = models.CharField('عنوان', max_length=30)
    star = models.ManyToManyField(User, verbose_name='ذخیره کردن', null=True, blank=True, related_name="post_star")
    image = models.ImageField('عکس پست', upload_to='post_images/')
    created_at = models.DateTimeField('زمان ایجاد پست', max_length=30, auto_now_add=True)
    updated_at = models.DateTimeField('زمان بروزرسانی پست', max_length=30, auto_now=True)
    activated = models.BooleanField('فعال شده', default=False)
    verificated = models.BooleanField('تاییدشده', default=False)
    category = models.ForeignKey(Category, verbose_name='دسته بندی', on_delete=models.CASCADE)
    labelpost = models.ManyToManyField(Label, verbose_name='برچسب',
                                       through='LabelPost',
                                       through_fields=('post', 'label'),

                                       )

    def verificated_comment_set(self):
        return self.comment_set.all().filter(verificated=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "پست ها"
        permissions = (
            ("can_verify", "Can verify post"),
            ("can_unverify", "Can unverify post"),
        )
        ordering = ['-created_at']


class Comment(Text):
    pub_date = models.DateTimeField('زمان انتشار', max_length=30, auto_now=True)
    created_date = models.DateTimeField('زمان ایجاد', max_length=30, auto_now_add=True)
    verificated = models.BooleanField('تاییدشده', default=False)
    post = models.ForeignKey(Post, verbose_name='پست', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "نظرات"
        ordering = ['-created_date']


class LabelPost(models.Model):
    post = models.ForeignKey(Post, verbose_name='پست', on_delete=models.CASCADE, related_name='post')
    label = models.ForeignKey(Label, verbose_name='برچسب', on_delete=models.CASCADE)

    def __str__(self):
        return self.post.text

    class Meta:
        verbose_name_plural = "برچسب های پست"
