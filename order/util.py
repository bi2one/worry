# -*- coding: utf-8 -*-
import sys

## Utility functions
def make_title(doll_count, phonedoll_count, is_gift) :
    orig_encoding = sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding("utf-8")

    ret_string = ""

    if is_gift and (doll_count != "0" or phonedoll_count != "0"):
        ret_string = "[선물]"

    if doll_count != "0":
        ret_string = ret_string + "다섯 걱정이 " + doll_count + "세트"
        if phonedoll_count != "0":
            ret_string = ret_string + ", 걱정이 핸드폰 줄 " + phonedoll_count + "세트"
    else :
        if phonedoll_count != "0":
            ret_string = ret_string + "걱정이 핸드폰 줄 " + phonedoll_count + "세트"
        else:
            ret_string = "주문 내용이 없습니다"

    sys.setdefaultencoding(orig_encoding)
    return ret_string
