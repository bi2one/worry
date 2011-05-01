# -*- encoding: utf-8 -*-
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = Library()
@register.filter
def make_state_readable(value):
    state_table = {"before_payment":"입금전",
                   "create":"제작중",
                   "send":"배송중",
                   "done":"배송완료",
                   "fail":"배송실패" }
    return state_table.get(str(value))
