from django.db.models.functions import Concat
from django.db.models import Value as V
from django.db.models import Q
from khayyam import JalaliDate

from .models import Post


def simple_search(query):
    qs_writer = Post.objects.annotate(full_name=Concat('user__first_name', V(' '), 'user__last_name')).filter(
        Q(full_name__regex=r'^.*{}.*'.format(query)))
    qs_text = Post.objects.filter(Q(text__regex=r'^.*{}.*'.format(query)))
    qs_title = Post.objects.filter(Q(title__regex=r'^.*{}.*'.format(query)))
    qs_label = Post.objects.filter(Q(labelpost__label_name__regex=r'^.*{}.*'.format(query))).distinct()
    context = {
        'posts_text': qs_text,
        'posts_title': qs_title,
        'posts_writer': qs_writer,
        'posts_label': qs_label,
    }
    return context


def advanced_search(q_label=None, q_title=None, q_text=None, q_writer=None, s_date=None,
                    e_date=None):
    query_set = Post.objects.annotate(full_name=Concat('user__first_name', V(' '), 'user__last_name'))
    if s_date:
        try:
            strt_date = s_date.split('/')
            from_date = JalaliDate(int(strt_date[0]), int(strt_date[1]), int(strt_date[2])).todate()
            query_set = query_set.filter(Q(created_at__gte=from_date))
        except:
            context = 'error'
            return context

    if e_date:
        try:
            end_date = e_date.split('/')
            to_date = JalaliDate(int(end_date[0]), int(end_date[1]), int(end_date[2]) + 1).todate()
            query_set = query_set.filter(Q(created_at__lte=to_date))
        except:
            context = 'error'
            return context
    if q_label:
        query_set = query_set.intersection(
            Post.objects.annotate(full_name=Concat('user__first_name', V(' '), 'user__last_name')).filter(
                Q(labelpost__label_name__regex=r'^.*{}.*'.format(q_label))))
    if q_text:
        query_set = query_set.intersection(
            Post.objects.annotate(full_name=Concat('user__first_name', V(' '), 'user__last_name')).filter(
                Q(text__regex=r'^.*{}.*'.format(q_text))))
    if q_writer:
        query_set = query_set.intersection(
            Post.objects.annotate(full_name=Concat('user__first_name', V(' '), 'user__last_name')).filter(
                Q(full_name__regex=r'^.*{}.*'.format(q_writer))))
    if q_title:
        query_set = query_set.intersection(
            Post.objects.annotate(full_name=Concat('user__first_name', V(' '), 'user__last_name')).filter(
                Q(title__regex=r'^.*{}.*'.format(q_title))))

    context = {
        'posts_advanced_search': query_set.order_by('-created_at'),
    }

    return context
