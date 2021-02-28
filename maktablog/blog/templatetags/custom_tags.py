from datetime import datetime, timedelta

import khayyam
from django import template
from khayyam import *

register = template.Library()


def convert_to_jdate(value):
    return JalaliDatetime(datetime(value.year, month=value.month, day=value.day, hour=value.hour, minute=value.minute,
                                   second=value.second, microsecond=value.microsecond,
                                   tzinfo=TehranTimezone())+timedelta(hours=3, minutes=30)).strftime('%C')


def count_verify_comments(value):
    return value.filter(verificated=True).count()


register.filter('count_verify_comments', count_verify_comments)
register.filter('convert_to_jdate', convert_to_jdate)
