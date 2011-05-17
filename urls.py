import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()
# print("aaaaaaaaaaaa");

urlpatterns = patterns('',
    (r'^index/$', 'django.views.generic.simple.direct_to_template', {'template':'index.html'}),
    (r'^intro/$', 'django.views.generic.simple.direct_to_template', {'template':'intro.html'}),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', {'template':'about.html', 'extra_context':{'about':True}}),
    (r'^traffic/$', 'django.views.generic.simple.direct_to_template', {'template':'traffic_view.html'}),

# Migration
#    (r'^mig_qna/', 'worry.file_manager.views.mig_qna'),
#    (r'^mig_worry/', 'worry.file_manager.views.mig_worry'),
#    (r'^mig_shop/', 'worry.file_manager.views.mig_shop'),
#    (r'^mig/', 'worry.file_manager.views.mig'),
#    (r'^mem/', 'worry.file_manager.views.mem'),
    (r'^admin/', include(admin.site.urls)),

#(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
# {'document_root': settings.MEDIA_ROOT}),

    # # order
    (r'^order/', include('worry.order.urls')),

    # # twitter
    (r'^twitter/', include('worry.twitter.urls')),

    # # i18n
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^(?P<module_name>\w+)/search/$', 'worry.search.views.search'),

    # # handle file upload & request
    (r'^file/(?P<file_id>\d+)$', 'worry.file_manager.views.serve_file'),
    (r'^upload/$', 'worry.file_manager.views.upload'),

    # # Accounts part
    (r'^accounts/mypage/$', 'worry.accounts.views.mypage'),
    (r'^accounts/mypage/(?P<page_number>\d+)/$', 'worry.accounts.views.mypage'),
    (r'^accounts/login/$', 'worry.accounts.views.login_user'),
    (r'^accounts/join/$', 'worry.accounts.views.join_user'),
    (r'^accounts/logout/$', 'worry.accounts.views.logout_user'),
    (r'^accounts/rpx$', 'worry.accounts.views.rpx'),
    (r'^join/$', 'worry.accounts.views.join_user'),
    (r'^check_username/$', 'worry.accounts.views.check_username'),

    # for index page
    (r'^/$', 'worry.document.views.frame'),
    (r'^$', 'worry.document.views.frame'),
#    (r'^index/$', 'worry.document.views.index'),

    # # others
    (r'^', include('worry.document.urls')),
    #(r'^$', 'worry.document.views.warning'),
)

