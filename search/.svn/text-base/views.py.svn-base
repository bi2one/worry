from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext


def search(request) :
    q = Q()
    if request.GET.has_key('query') :
        query = request.GET['query'].strip()
        keywords = query.split()
        for keyword in keywords :
#             q = q | Q(content__icontains=keyword)
#             q = q | Q(user__username__icontains=keyword)
#             q = q | Q(title__icontains=keyword)
            if request.GET.has_key('username') :
                q = q | Q(user__username__icontains=keyword)
                q = q | Q(user__nick_name__icontains=keyword)
            if request.GET.has_key('content') :
                q = q | Q(content__icontains=keyword)
            if request.GET.has_key('title') :
                q = q | Q(title__icontains=keyword)
    return q
