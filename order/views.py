# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

from worry.order.models import Bank, Order, Address
from worry.order.forms import OrderFormFirst, OrderFormSecond

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def form1(request):
    " order first form "
    form = OrderFormFirst()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('order_form_first.html', variables, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def form2(request) :
    if request.method == 'POST':
        # form1으로부터의 POST요청이 들어왔을 때(정상적인 form2접근일 때)
        form = OrderFormFirst(request.POST)

        if form.is_valid():
            sender_name = form.cleaned_data['sender_name']
            sender_phone = form.cleaned_data_phone()
            doll_count = form.cleaned_data['doll_count']
            phonedoll_count = form.cleaned_data['phonedoll_count']
            content = form.cleaned_data['content']

            default_data = {
                'sender_name': sender_name,
                'sender_phone': sender_phone,
                'doll_count': doll_count,
                'phonedoll_count': phonedoll_count,
                'content': content,
                'bank': 1,
                }
            form = OrderFormSecond(default_data)

            variables = RequestContext(request, {
                'form': form,
                'is_first': True
            })
            return render_to_response('order_form_second.html', variables, context_instance=RequestContext(request))
        else:
            # form1이 틀렸거나 올바른 form2 요청이 아닐 때
            variables = RequestContext(request, {
                'form': form
                })
            return render_to_response('order_form_first.html', variables, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/intro/')


@user_passes_test(lambda u: u.has_perm('document.can_add'))
def submit(request):
    if request.method == 'POST':
        form = OrderFormSecond(request.POST)
        
        if form.is_valid() :
            bank_id = form.cleaned_data['bank']
            sender_name = form.cleaned_data['sender_name']
            sender_phone = form.cleaned_data['sender_phone']
            doll_count = form.cleaned_data['doll_count']
            phonedoll_count = form.cleaned_data['phonedoll_count']
            content = form.cleaned_data['content']
            payment_name = form.cleaned_data['payment_name']
            receiver_name = form.cleaned_data['receiver_name']
            receiver_phone = form.cleaned_data_receiver_phone()
            receiver_address = form.cleaned_data_receiver_address()
            receiver_address_number = form.cleaned_data['receiver_address_number']
            send_issue = form.cleaned_data['send_issue']
            state = 'before_payment'
            bank = Bank.objects.get(id=bank_id)
            
            order = Order(
                user = request.user,
                bank = bank,
                sender_name = sender_name,
                sender_phone = sender_phone,
                doll_count = doll_count,
                phonedoll_count = phonedoll_count,
                content = content,
                payment_name = payment_name,
                receiver_name = receiver_name,
                receiver_phone = receiver_phone,
                receiver_address = receiver_address,
                receiver_address_number = receiver_address_number,
                send_issue = send_issue,
                state = state)
            order.save()
            return HttpResponseRedirect('/accounts/mypage/')
        else:
            variables = RequestContext(request, {
                'form': form
                })
            return render_to_response('order_form_second.html', variables, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/intro/')

def ajax_address_number(request):
    def addr_append(base, address_field):
        if address_field != "":
            base = base + " " + address_field
        return base
    
    if request.method == 'POST':
        search_segment = request.POST['search-text']
        print search_segment
        addresses = Address.objects.filter(DONG__contains=search_segment).order_by('-SEQ')

        ret_data = []
        for address in addresses :
            address_str = ""
            address_str = addr_append(address_str, address.SIDO)
            address_str = addr_append(address_str, address.GUGUN)
            address_str = addr_append(address_str, address.DONG)
            address_str = addr_append(address_str, address.RI)
            address_str = addr_append(address_str, address.BLDG)
            address_str = addr_append(address_str, address.BUNJI)
            
            ret_data.append({
                "ZIPCODE": address.ZIPCODE,
                "address": address_str
                })

        return HttpResponse(simplejson.dumps(ret_data))
    else:
        return HttpResponseRedirect('/intro/')
