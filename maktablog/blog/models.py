from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField

from PIL import Image


class UserInfo(models.Model):
    # first_name = models.CharField('نام', max_length=30, blank=True)
    # last_name = models.CharField('نام خانوادگی', max_length=30, blank=True)
    alias_name = models.CharField('نام مستعار', max_length=30)
    phone_number = models.CharField('شماره تلفن', max_length=11)
    image = models.ImageField('عکس پروفایل', upload_to='images/', null=True, blank=True)
    user = models.OneToOneField(User, verbose_name='کاربر', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            if img.height > 50 or img.width > 50:
                output_size = (50, 50)
                img.thumbnail(output_size)
                img.save(self.image.path)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.user.first_name

    class Meta:
        # verbose_name = "پروفایل کاربری"
        verbose_name_plural = "پروفایل کاربران"


@receiver(post_save, sender=User)
def update_userinfo_signal(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)
    instance.userinfo.save()


class MyModel(models.Model):
    content = HTMLField()

    def __str__(self):
        return self.content


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
    category_name = models.CharField('دسته بندی', max_length=30)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_sub', null=True,
                                 blank=True)

    def __str__(self):
        return self.category_name

    class Meta:
        # verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Label(models.Model):
    label_name = models.CharField('برچسب', max_length=30)

    def __str__(self):
        return self.label_name

    class Meta:
        # verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"


class Post(Text):
    title = models.CharField('عنوان', max_length=30)
    # star = models.BooleanField('ذخیره کردن', default=False)
    star = models.ManyToManyField(User, verbose_name='ذخیره کردن', null=True, blank=True, related_name="post_star")
    image = models.ImageField('عکس پست', upload_to='post_images/')
    created_at = models.DateTimeField('زمان ایجاد پست', max_length=30, auto_now_add=True)
    updated_at = models.DateTimeField('زمان بروزرسانی پست', max_length=30, auto_now=True)
    activated = models.BooleanField('فعال/غیرفعال', default=False)
    verificated = models.BooleanField('تایید کردن محتوای پست', default=False)
    category = models.ForeignKey(Category, verbose_name='دسته بندی', on_delete=models.CASCADE)
    # like = models.ForeignKey(Like, verbose_name='پسندیدن/نپسندیدن', on_delete=models.CASCADE)
    # user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    labelpost = models.ManyToManyField(Label,
                                       through='LabelPost',
                                       through_fields=('post', 'label'),

                                       )

    def verificated_comment_set(self):
        return self.comment_set.all().filter(verificated=True)

    def __str__(self):
        return self.text

    class Meta:
        # verbose_name = "پست"
        verbose_name_plural = "پست ها"
        permissions = (
            ("can_verify", "Can verify post"),
            ("can_unverify", "Can unverify post"),
        )
        ordering = ['-created_at']


class Comment(Text):
    # text = models.TextField('متن نظر')
    pub_date = models.DateTimeField('زمان انتشار', max_length=30, auto_now=True)
    # date_pub = models.DateTimeField('زمان بروزرسانی پست', max_length=30, auto_now=True)
    created_date = models.DateTimeField('زمان ایجاد', max_length=30, auto_now_add=True)
    verificated = models.BooleanField('تایید کردن محتوای نظر', default=False)
    # user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='پست', on_delete=models.CASCADE)

    # like = models.ForeignKey(Like, verbose_name='پسندیدن/نپسندیدن', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        # verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_date']


class LabelPost(models.Model):
    post = models.ForeignKey(Post, verbose_name='پست', on_delete=models.CASCADE, related_name='post')
    label = models.ForeignKey(Label, verbose_name='برچسب', on_delete=models.CASCADE)

    def __str__(self):
        return self.post.text

    class Meta:
        # verbose_name = "برچسب-پست"
        verbose_name_plural = "برچسب های پست"
