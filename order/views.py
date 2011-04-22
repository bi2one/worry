from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from django.db.models import Q
from worry.order.models import Bank, Order

from worry.order.forms import OrderFormFirst


@user_passes_test(lambda u: u.has_perm('document.can_add'))
def form1(request):
    " order first form "
    form = OrderFormFirst(initial = {'doll_count': 0, 'phonedoll_count': 0})

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('order_form_first.html', variables)
