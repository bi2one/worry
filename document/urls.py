from django.conf.urls.defaults import *
from django.conf import settings

import os

urlpatterns = patterns('worry.document.views',
    (r'^tag/(?P<tag_name>.*)/$', 'tag'),
#     (r'^worryboard/$', 'worryboard'),
#     (r'^worryboard/(?P<page_number>\d+)/$', 'worryboard'),
#     (r'^shop/$', 'shop'),
#     (r'^shop/(?P<page_number>\d+)/$', 'shop'),
#     (r'^blog/$', 'blog'),
#     (r'^guest/$', 'guest'),
#     (r'^blog/(?P<page_number>\d+)/$', 'blog'),
#     (r'^guest/(?P<page_number>\d+)/$', 'blog'),
#     (r'^test_write/$', 'test_write'),

    # comment
    (r'^comment_reply/(?P<doc_id>\d+)/$', 'reply_comment'),
    (r'^edit_comment/(?P<comment_id>\d+)/$', 'edit_comment'),
    # (r'^comment_reply/(?P<doc_id>\d+)/$', 'reply_comment'),
    # (r'^edit_comment/(?P<comment_id>\d+)/$', 'edit_comment'),
    (r'^write_comment/(?P<doc_id>\d+)/$', 'write_comment'),
    (r'^delete_comment/(?P<comment_id>\d+)/$', 'delete_comment'),

    (r'^(?P<module_name>\w+)/$', 'entry'),
    (r'^(?P<module_name>\w+)/(?P<page_number>\d+)/$', 'entry'),
    (r'^(?P<module_name>\w+)/view/(?P<doc_id>\d+)/$', 'view'),

    (r'^(?P<module_name>\w+)/view/$', 'view'),
    (r'^(?P<module_name>\w+)/modify/(?P<doc_id>\d+)/$$', 'save'),
    (r'^(?P<module_name>\w+)/write_comment/(?P<doc_id>\d+)/$$', 'write_comment'),
    # (r'^(?P<module_name>\w+)/write_comment/(?P<doc_id>\d+)/?P<cmt_id>\d+)/$$', 'write_comment'),
    (r'^(?P<module_name>\w+)/write/$', 'write'),
    (r'^(?P<module_name>\w+)/delete/(?P<doc_id>\d+)/$', 'delete'),
    (r'^(?P<module_name>\w+)/save/$', 'save'),

                       
)
