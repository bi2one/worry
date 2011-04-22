from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect

from django.db.models import Q
from worry.order.models import Bank, Order

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def form1(request):
    
