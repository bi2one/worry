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
)
