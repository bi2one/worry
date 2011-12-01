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
                   "create":"탄생중",
                   "send":"배송중",
                   "done":"배송완료",
                   "fail":"배송실패" }
    return state_table.get(str(value))

@register.filter
def pp_delay_date(month, day):
    result = "지금 주문하시면, "
    if month == 0:
        if day == 0:
            return result + " 소요기간이 특별히 걸리지 않습니다."
    else:
        result = result + str(month) + "달"

    if day == 0:
        pass
    else:
        result = result + " " + str(day) + "일"

    result = result + " 정도 소요됩니다."
    return result

