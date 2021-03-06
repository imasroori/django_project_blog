# Generated by Django 3.1.4 on 2021-03-03 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20210220_1255'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyModel',
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_date'], 'verbose_name_plural': 'نظرات'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at'], 'permissions': (('can_verify', 'Can verify post'), ('can_unverify', 'Can unverify post')), 'verbose_name_plural': 'پست ها'},
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_sub', to='blog.category', verbose_name='زیرمجموعه'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=30, verbose_name='نام دسته بندی'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='verificated',
            field=models.BooleanField(default=False, verbose_name='تاییدشده'),
        ),
        migrations.AlterField(
            model_name='post',
            name='activated',
            field=models.BooleanField(default=False, verbose_name='فعال شده'),
        ),
        migrations.AlterField(
            model_name='post',
            name='labelpost',
            field=models.ManyToManyField(through='blog.LabelPost', to='blog.Label', verbose_name='برچسب'),
        ),
        migrations.AlterField(
            model_name='post',
            name='verificated',
            field=models.BooleanField(default=False, verbose_name='تاییدشده'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='image',
            field=models.ImageField(blank=True, default='images/default/default-avatar.jpg', null=True, upload_to='images/', verbose_name='عکس پروفایل'),
        ),
    ]
