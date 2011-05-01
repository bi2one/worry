# -*- encoding: utf-8 -*-
# Create your views here.
from django.contrib.auth import authenticate, login, logout
# from django.views.decorators.cache import never_cache
# from django.views.decorators.cache import cache_control

from django.contrib.auth.forms import AuthenticationForm
from worry.accounts.forms import JoinForm
from worry.document.util import *
from worry.order.models import Bank, Order
from worry.pagination.views import pagination

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist

import json


import urllib
import urllib2
import re

# LOGIN Part
def check_rpx_user_or_create(profile) :
    identifier = profile['identifier']
    name = profile.get('displayName')
    email = profile.get('email')
    try:
        user = User.objects.get(username=identifier)
    except User.DoesNotExist:
        group = Group.objects.get(name="auth_user")
        user = User(username=identifier, nick_name=name, email=email, is_rpx=True)
        user.save()
        user.groups.add(group)
        user.save()


def rpx(request):
    if request.method == 'POST' :
        token = request.POST['token']
        api_params = {
            'token': token,
            'apiKey': 'ed083f48c31604d68ed2019daeb53e41814b830e',
            'format': 'json',
        }
        http_response = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info', urllib.urlencode(api_params))
        # python 2.6
        #         auth_info_json = http_response
        #         auth_info = json.load(auth_info_json)

        # Older version python 2.5 etc.. json
        auth_info_json = http_response
        auth_info = json.load(auth_info_json)

        if auth_info['stat'] == 'ok':
            profile = auth_info['profile']
            identifier = profile['identifier'] # Unique ID
            check_rpx_user_or_create(profile)
            return login_user(request, username=identifier, is_rpx=True)
        else:
            return HttpResponse('An error occured: ' + auth_info['err']['msg'])
    else :
        redirect_to = request.REQUEST.get('next', '')
        if not redirect_to :
            redirect_to = '/?next=/intro';
        else :
            redirect_to = '/?next=' + redirect_to
        return HttpResponseRedirect(redirect_to)


def login_user(request, username=None,is_rpx=None) :
    is_error = False

    if request.GET.has_key('next') : redirect_to = request.GET['next']
    else: redirect_to = request.REQUEST.get('next', '')
    if not redirect_to :
        redirect_to = get_referer(request)
#    redirect_to = '/?next=' + redirect_to

    # RPX Login
    if is_rpx :
        redirect_to = '/?next=' + redirect_to
        user = authenticate(username=username, password=None, is_rpx=True)
        if user is not None :
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
            else :
                return HttpResponseRedirect(redirect_to)
        else :
            return HttpResponseRedirect(redirect_to)

    # Normal login
    elif request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponseRedirect(redirect_to)
        else:
            is_error = True

    form = AuthenticationForm(request)

    variables = RequestContext(request, {
        'next' : redirect_to,
        'is_error': is_error,
        'form': form
    })

    return render_to_response('registration/login.html',
                              variables,
                              context_instance=RequestContext(request))


def logout_user(request) :
    logout(request)
    response = HttpResponseRedirect('/intro/')
    response.delete_cookie('user_location')
    return response

# def logout_user(request):
#      response = logout(request, next_page=reverse('app.home.views.home'))
#      response.delete_cookie('user_location')
#      return response

def join_user(request) :
    if request.method == 'POST':
        form = JoinForm(request.POST)

        if form.is_valid():
            # save user
            group = Group.objects.get(name="auth_user")
            username = form.cleaned_data['username']
            nick_name = form.cleaned_data['nick_name']
            password = form.cleaned_data['password']
            user = User(
                username = username,
                nick_name = nick_name,
                password = '',
                email = form.cleaned_data['email']
            )
            user.set_password(password)
            user.save()
            user.groups.add(group)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/intro/')
            # return login_user(request)
    else:
        form = JoinForm()

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'join.html',
        variables
    )

def check_username(request):
    if request.is_ajax():
        username = request.POST['username']
        if not re.search(r'^[a-zA-Z][a-zA-Z0-9]*$', username):
            return HttpResponse('사용자 아이디는 알파벳으로 시작하고, 기호가 들어갈 수 없습니다.')
        else:
            try:
                User.objects.get(username=username)
            except ObjectDoesNotExist:
                return HttpResponse('사용 가능한 아이디입니다.')
            return HttpResponse('이미 사용중인 아이디 입니다.')
    return HttpResponse('')

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def mypage(request, page_number=1):
    user = request.user
    orders = Order.objects.all().order_by('-pub_date')

    variables = {}
    if (len(orders) != 0) :
        recent_order = orders[0]
        variables = pagination(request, orders, page_number, 2)

        if recent_order.state != "done" and recent_order.state != "fail":
            variables.update({'recent_order': recent_order})
    
    variables.update({
        'user': user,
        })

    return render_to_response(
        'mypage.html',
        variables,
        context_instance=RequestContext(request))
