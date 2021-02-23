from datetime import datetime

import khayyam
from django import template
from khayyam import *

register = template.Library()


def convert_to_jdate(value):
    return JalaliDatetime(datetime(value.year, value.month, value.day, value.hour, value.minute,
                                   value.second, 821830, TehranTimezone())).strftime('%C')


def count_verify_comments(value):
    return value.filter(verificated=True).count()


register.filter('count_verify_comments', count_verify_comments)
register.filter('convert_to_jdate', convert_to_jdate)
