import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template

# admin.autodiscover()

urlpatterns = patterns('',
    (r'^form1/$', 'worry.order.views.form1'),
    (r'^form2/$', 'worry.order.views.form2'),
    (r'^submit/$', 'worry.order.views.submit'),
    (r'^ajax_address_number/$', 'worry.order.views.ajax_address_number'),
    (r'^modify/(?P<order_id>\d+)/$', 'worry.order.views.modify'),
    (r'^admin/$', 'worry.order.views.admin'),
    (r'^admin/(?P<page_number>\d+)$', 'worry.order.views.admin'),
    (r'^admin/(?P<page_number>\d+)/$', 'worry.order.views.admin'),
    (r'^admin/(?P<page_number>\d+)/(?P<state>\w+)$', 'worry.order.views.admin'),
    (r'^admin/view/(?P<order_id>\d+)/$', 'worry.order.views.admin_view'),
    (r'^delete/(?P<order_id>\d+)/$', 'worry.order.views.delete'),
)
