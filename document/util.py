# -*- encoding: utf-8 -*-
from django.conf import settings
from worry.file_manager.models import File
from urllib import quote_plus
from django.core import mail
# from django.core.mail import send_mail

## Utility functions
def get_option_string(request) :
    ret = []
    # if request.GET.has_key('page_number') :
    #     ret.append('page_number='+request.GET['page_number'])
    if request.GET.has_key('category') :
        ret.append('category='+request.GET['category'])
    if request.GET.has_key('query') :
        ret.append('query='+quote_plus(request.GET['query'].encode('utf-8')))
    if request.GET.has_key('username') :
        ret.append('username')
    if request.GET.has_key('title') :
        ret.append('title')
    if request.GET.has_key('content') :
        ret.append('content')

    if ret == [] :
        return ''
    else :
        return '?' + '&'.join(ret)

def get_module_id(module_name) :
    return settings.MODULE_ID[module_name]

def get_category_id(module_name, category_name) :
    if module_name == 'blog' :
        return settings.BLOG_CATEGORY_ID[category_name]
    elif module_name == 'board':
        return settings.BOARD_CATEGORY_ID[category_name]

def get_category_name(module_name, category) :
    if module_name == 'blog' :
        return settings.BLOG_CATEGORY_NAME[int(category)]
    elif module_name == 'board':
        return settings.BOARD_CATEGORY_NAME[int(category)]

def get_canonical_module_name(module_name) :
    if module_name == 'shop' or module_name == 'worryboard' or module_name == 'faq' or module_name == 'notice' :
        return 'board'
    elif module_name == 'guest' :
        return 'guest'
    else :
        return 'blog'

def get_referer(request) :
    if request.META.has_key('HTTP_REFERER') :
        return request.META['HTTP_REFERER']
    else :
        return None

def get_ipaddress(request) :
    if request.META.has_key('REMOTE_ADDR') :
        return request.META['REMOTE_ADDR']
    else :
        return ""

def handle_uploaded_files(document, file_list, file_type) :
    if len(file_list) > 0 :
        file_list = file_list[:-1].strip() # strip last comma
        for file_id in file_list.split(',') :
            f = File.objects.get(id=file_id)
            f.document = document;
            f.file_type = file_type
            f.save()

def get_cmt_padding(max_indent=5, padding_gap=8):
    return [x * padding_gap for x in range(max_indent + 1, 1, -1)]

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def sendNewPasswordMail(return_url, to_email):
    subject = "돈워리컴퍼니 비밀번호 변경"
    body = "아래 링크로 연결해 주세요.\n\n" + return_url
    email = mail.EmailMessage(subject, body, 'dontworrycompany@gmail.com', [to_email])
    email.send()
