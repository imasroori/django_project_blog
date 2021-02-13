from datetime import datetime

import khayyam
from django import template
from khayyam import *

register = template.Library()


def convert_to_jdate(value):
    return JalaliDatetime(datetime(value.year, value.month, value.day, value.hour, value.minute,
                                   value.second, 821830, TehranTimezone())).strftime('%C')
    # return JalaliDatetime(datetime(2015, 7, 22, 14, 47, 9, 821830, TehranTimezone()))


register.filter('convert_to_jdate', convert_to_jdate)
