# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson

from worry.order.models import Bank, Order, Address, Delay
from worry.order.util import *
from worry.document.models import Document
from worry.document.util import *
from worry.order.forms import OrderFormFirst, OrderFormSecond, OrderFormModify, OrderFormState, InsertDelayForm
from worry.pagination.views import pagination

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def form1(request):
    " order first form "
    form = OrderFormFirst()

    delays = Delay.objects.all()
    if len(delays) == 0:
        month = 0
        day = 0
    else:
        delay = delays[0]
        month = delay.month
        day = delay.day
    
    variables = RequestContext(request, {
        'form': form,
        'delay_month': month,
        'delay_day': day,
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
            receiver_address = form.cleaned_data['receiver_address']
            receiver_detail_address = form.cleaned_data['receiver_detail_address']
            receiver_address_number = form.cleaned_data['receiver_address_number']
            send_issue = form.cleaned_data['send_issue']
            is_gift = form.cleaned_data['is_gift']
            state = 'before_payment'
            bank = Bank.objects.get(id=bank_id)
            module_name = get_canonical_module_name("shop")
            category = 2

            document = Document(
                user = request.user,
                module_id = get_module_id(module_name),
                module_name = module_name,
                category = category,
                category_name = get_category_name(module_name, category),
                is_notice = False,
                title = make_title(doll_count, phonedoll_count, is_gift),
                content = "",
                ipaddress = get_ipaddress(request),
                hit=0)
            document.save()
            
            order = Order(
                user = request.user,
                bank = bank,
                document  = document,
                sender_name = sender_name,
                sender_phone = sender_phone,
                doll_count = doll_count,
                phonedoll_count = phonedoll_count,
                content = content,
                payment_name = payment_name,
                receiver_name = receiver_name,
                receiver_phone = receiver_phone,
                receiver_address = receiver_address,
                receiver_detail_address = receiver_detail_address,
                receiver_address_number = receiver_address_number,
                send_issue = send_issue,
                is_gift = is_gift,
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

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def modify(request, order_id):
    order = Order.objects.get(id=order_id)

    # validation check
    if order.user.id != request.user.id or (order.state != "before_payment" and order.state != "create"):
        return HttpResponseRedirect('/intro/')

    if request.method == 'POST':
        form = OrderFormModify(request.POST)
        
        if form.is_valid() :
            doll_count = form.cleaned_data["doll_count"]
            phonedoll_count = form.cleaned_data["phonedoll_count"]
            content = form.cleaned_data["content"]
            bank_id = form.cleaned_data["bank"]
            bank = Bank.objects.get(id=bank_id)
            payment_name = form.cleaned_data['payment_name']
            receiver_name = form.cleaned_data['receiver_name']
            receiver_phone = form.cleaned_data_receiver_phone()
            receiver_address_number = form.cleaned_data['receiver_address_number']
            receiver_address = form.cleaned_data['receiver_address']
            receiver_detail_address = form.cleaned_data['receiver_detail_address']
            is_gift = form.cleaned_data['is_gift']

            order.doll_count = doll_count
            order.phonedoll_count = phonedoll_count
            order.content = content
            order.bank = bank
            order.payment_name = payment_name
            order.receiver_name = receiver_name
            order.receiver_phone = receiver_phone
            order.receiver_address_number = receiver_address_number
            order.receiver_address = receiver_address
            order.receiver_detail_address = receiver_detail_address
            order.is_gift = is_gift
            doc = order.document
            
            doc.title = make_title(doll_count, phonedoll_count, is_gift)

            doc.save()
            order.save()
            
            return HttpResponseRedirect('/accounts/mypage/')
        else:
            variables = RequestContext(request, {
                'order_id': order_id,
                'form': form
                })
            return render_to_response('order_modify.html', variables, context_instance=RequestContext(request))
    else :
        receiver_phone = order.receiver_phone.split('-')
        receiver_address = order.receiver_address.split('//')
        
        default_data = {
            'sender_name': order.sender_name,
            'sender_phone': order.sender_phone,
            'doll_count': order.doll_count,
            'phonedoll_count': order.phonedoll_count,
            'content': order.content.replace('<br>', '\n'),
            'bank': order.bank.id,
            'payment_name': order.payment_name,
            'receiver_name': order.receiver_name,
            'receiver_phone_1': receiver_phone[0],
            'receiver_phone_2': receiver_phone[1],
            'receiver_phone_3': receiver_phone[2],
            'receiver_address_number': order.receiver_address_number,
            'receiver_address': order.receiver_address,
            'receiver_detail_address': order.receiver_detail_address,
            'is_gift': order.is_gift,
            }
        
        form = OrderFormModify(default_data)
        
        variables = RequestContext(request, {
            'order_id': order_id,
            'form': form
            })
        return render_to_response('order_modify.html', variables, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def admin(request, page_number=1, state=""):
    user = request.user
    form = InsertDelayForm({
        'month':0,
        'day':0,
        })

    delays = Delay.objects.all()
    if len(delays) == 0:
        month = 0
        day = 0
    else:
        delay = delays[0]
        month = delay.month
        day = delay.day
    
    # validation check
    if not user.is_superuser :
        raise Http404

    if request.method == 'POST' :
        form = InsertDelayForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            day = form.cleaned_data['day']
            delay = Delay(month=month, day=day)
            Delay.objects.all().delete()
            delay.save()

    if state == "":
        orders = Order.objects.all().order_by('-pub_date')
    else:
        orders = Order.objects.filter(state=state).order_by('-pub_date')

    variables = pagination(request, orders, page_number, 30)
    variables.update({
        'form':form,
        'month':month,
        'day':day,
        'state':state,
        })
    
    return render_to_response(
        'order_admin.html',
        variables,
        context_instance=RequestContext(request))

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def admin_view(request, order_id):
    user = request.user

    # validation check
    if not user.is_superuser :
        raise Http404

    order = Order.objects.get(id=order_id)
    form = OrderFormState({'state': order.state,
                           'invoice_number': order.invoice_number})
    if request.method == 'POST':
        form = OrderFormState(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            invoice_number = form.cleaned_data['invoice_number']
            order.invoice_number = invoice_number
            order.state = state
            order.save()

            variables = {
                "order": order,
                "form": form,
                }

            return render_to_response(
                'order_admin_view.html',
                variables,
                context_instance=RequestContext(request))
        
    variables = {
        "order": order,
        "form": form,
        }
    return render_to_response(
        'order_admin_view.html',
        variables,
        context_instance=RequestContext(request))
        
@user_passes_test(lambda u: u.has_perm('document.can_add'))
def delete(request, order_id):
    user = request.user

    if not user.is_superuser :
        raise Http404

    order = Order.objects.get(id=order_id)
    order.document.delete()
    return HttpResponseRedirect('/order/admin/')
