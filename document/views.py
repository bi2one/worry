from django.conf import settings

from django.contrib.auth.views import logout

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import User, Group
from worry.document.util import *
from django.db.models import Q

from worry.pagination.views import pagination
from worry.search.views import *

from worry.document.models import Document, Comment, Tag
from worry.document.forms import WriteForm, GuestBookForm, WriteCommentForm, GuestWriteForm, GuestWriteCommentForm
from worry.accounts.forms import JoinForm

from worry.twitter.views import save_tweet
import random

def frame(request) :
    if request.GET.has_key('next') :
        redirect_to = request.REQUEST.get('next', request.GET['next'])
    else :
        redirect_to = request.REQUEST.get('next', '/index')
    return render_to_response('frame.html' , {'next':redirect_to},
                              context_instance=RequestContext(request))


def tag(request, tag_name) :
    tag = get_object_or_404(Tag, name=tag_name)
    docs = tag.documents.order_by('-id')
    variables = RequestContext(request, {
        'docs' : docs,
        'tag_name': tag_name,
    })
    return render_to_response('tag_page.html', variables)

def entry(request, module_name, page_number=1) :
    canonical_module_name = get_canonical_module_name(module_name)
    module_id = get_module_id(canonical_module_name)

    q = Q(module_id=module_id)
    # if not request.user.is_superuser:
    #     q = q & (Q(is_secret=False) | Q(user=request.user.id))
        
    docs = Document.objects.filter(q).order_by('-is_notice','-id')
    category = None
    category_name = None
    if request.GET.has_key('category') :
        category = request.GET['category']
        if category != '' and category != 'None':
            category_name = get_category_name(canonical_module_name, category)
            docs = docs.filter(category=category)
        else : pass

    docs = docs.filter(search(request))

    if str(module_name) == 'blog' :
        variables = pagination(request, docs, page_number, 10)
    elif str(module_name) == "shop" :
        variables = pagination(request, docs, page_number, 15)
    else :
        variables = pagination(request, docs, page_number)


    variables.update({'category_name':category_name,
                      'category':category,
                      'page_number':int(page_number),
                      'module_name':module_name,
                      'option_string' : get_option_string(request)
                      })
    return render_to_response(canonical_module_name + '.html', variables,
                              context_instance=RequestContext(request))

## Document CRUD
def write_guest_book(request, module_name, is_secret) :
    " Guest book write "
    canonical_module_name = get_canonical_module_name(module_name)
    module_id = get_module_id(canonical_module_name)

    if request.GET.has_key('docid'):
        if isNumber(request.GET['docid']):
            return save(request, module_name, request.GET['docid'])

    form = GuestBookForm(request.POST)
    if form.is_valid() :
        doc = Document(
            user = request.user,
            module_id=module_id,
            module_name=canonical_module_name,
            content = form.cleaned_data['tx_content'],
            is_secret = is_secret,
            ipaddress = get_ipaddress(request),
            hit=0)
        doc.save()
        if not is_secret :
            save_tweet(doc)
    else:
        form = GuestBookForm()

    return HttpResponseRedirect("/guest/")
    
def write_document(request, module_name, is_secret) :
    " blog, board write "
    canonical_module_name = get_canonical_module_name(module_name)
    module_id = get_module_id(canonical_module_name)

    if request.POST.has_key('is_notice') : is_notice = True
    else : is_notice = False

    form = WriteForm(request.POST)
    if form.is_valid() :
        category = None
        category_name = None
        if request.POST.has_key('tx_article_category') :
            category = request.POST['tx_article_category']
            category_name = get_category_name(canonical_module_name, request.POST['tx_article_category'])

            doc = Document(
                user = request.user,
                module_id=module_id,
                module_name=canonical_module_name,
                
                category = category,
                category_name = category_name,
                is_notice = is_notice,
                title = form.cleaned_data['tx_article_title'],
                content = form.cleaned_data['tx_content'],
                is_secret = is_secret,
                ipaddress = get_ipaddress(request),
                hit=0)
            doc.save()
            # twitter
            if request.POST.has_key('twitter') :
                save_tweet(doc)
            
            # Save tags
            # print form.cleaned_data['tags']
            tag_names = form.cleaned_data['tags'].split(',')
            
            for tag_name in  tag_names:
                tag_name = tag_name.strip()
                if tag_name == '' : continue
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                doc.tag_set.add(tag)
            doc.save()
                
            handle_uploaded_files(document = doc,
                                  file_list = request.POST['attach_files'],
                                  file_type = settings.FILE_TYPE)
            
            handle_uploaded_files(document = doc,
                                  file_list = request.POST['attach_images'],
                                  file_type = settings.IMAGE_TYPE)

            if module_name == 'blog':
                return HttpResponseRedirect("/%s/?category=%d" % (module_name, int(category)))
            else:
                return HttpResponseRedirect("/%s/%s/%d/?category=%d" % (category_name, "view", doc.id, int(category)))
            
        else :
            return HttpResponseRedirect(get_referer(request))

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def write(request, module_name) :
    " general write facade view "
    doc=None
    category=None

    canonical_module_name = get_canonical_module_name(module_name)
    module_id = get_module_id(canonical_module_name)

    if canonical_module_name == 'board' :
        category = get_category_id(canonical_module_name, module_name)

    if request.method == 'POST' or module_name == 'guest':
        if request.POST.has_key('is_secret') : is_secret = True
        else : is_secret = False
        if module_name == 'guest' :
            return write_guest_book(request, module_name, is_secret)
        else :
            return write_document(request, module_name, is_secret)
    else :
        form = WriteForm()


    if request.META.has_key('HTTP_HOST') :
        host = request.META.get('HTTP_HOST')
    else :
        host = "dontworryworry.com"

    return render_to_response('write.html', {
            'host' : host,
            'doc' : doc,
            'form' :form,
            'module_name' : module_name,
            'category' : category,
            },
            context_instance=RequestContext(request))

@user_passes_test(lambda u: u.has_perm('document.can_delete'))
def delete(request, module_name, doc_id) :
    user = request.user
    canonical_module_name = get_canonical_module_name(module_name)
    if canonical_module_name == 'blog' :
        category = ''
    else:
        category = get_category_id(canonical_module_name, module_name)
    doc = Document.objects.get(id=doc_id)

    if not user.is_superuser : 
        if doc.user :
            if doc.user.id != user.id :
                # TODO : invalid message
                return HttpResponseRedirect('/' + module_name)
            else :
                doc.delete()
                return HttpResponseRedirect('/' + module_name)
        else :
            return HttpResponseRedirect('/' + module_name)
    else :
        doc.delete()
        if canonical_module_name == 'guest':
            return HttpResponseRedirect('/guest/')
        return HttpResponseRedirect('/'+module_name+'/?category='+str(category)) ## REDIRECT TO WHERE?



@user_passes_test(lambda u: u.has_perm('document.can_change'))
def save(request, module_name, doc_id) :
    user = request.user
    doc = Document.objects.get(id=doc_id)
    canonical_module_name = get_canonical_module_name(module_name)

    if not user.is_superuser : 
        if doc.user :
            if doc.user.id != user.id :
                # TODO : invalid message
                return HttpResponseRedirect('/' + module_name)
        else :
            return HttpResponseRedirect('/' + module_name)

    if request.method == 'POST' : ## Check user ownership
        # print request.POST.keys()
        if canonical_module_name == 'guest' :
            form = GuestWriteForm(request.POST)
            if form.is_valid() :
                doc = Document.objects.get(id=doc_id)
                doc.content = form.cleaned_data['tx_content']
                doc.is_secret = form.cleaned_data['is_secret']
                doc.save()
                return HttpResponseRedirect("/" + module_name + "/")
            else :
                return HttpResponseRedirect(get_referer(request))
        form = WriteForm(request.POST)
        category = None
        if form.is_valid() :
            category = form.cleaned_data['tx_article_category']
            doc = Document.objects.get(id=doc_id)
            doc.title = form.cleaned_data['tx_article_title']
            doc.content = form.cleaned_data['tx_content']
            doc.is_secret = form.cleaned_data['is_secret']
            doc.category = category
            doc.category_name = get_category_name(canonical_module_name, category)
            doc.is_notice = form.cleaned_data['is_notice']
            doc.save()

            # Save tags
            doc.tag_set.clear()

            # print form.cleaned_data['tags']
            tag_names = form.cleaned_data['tags'].split(',')
            for tag_name in tag_names :
                tag_name = tag_name.strip()
                if tag_name == '' : continue
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                doc.tag_set.add(tag)
            doc.save()

            if module_name == 'blog':
                return HttpResponseRedirect("/" + module_name + '/?category=' + category)
            else :
                return HttpResponseRedirect("/" + module_name + "/view/" + doc_id +"/?category=" + category)
        return HttpResponseRedirect(get_referer(request))
    else :
        form = WriteForm()
        tags = doc.tag_set.all()


        if request.META.has_key('HTTP_HOST') :
            host = request.META.get('HTTP_HOST')
        else :
            host = "dontworryworry.com"

        data = {
            'host': host,
            'doc' : doc,
            'tags' : tags,
            'form' : form, 
            'category' : doc.category_name,
            'module_name' : module_name
            }
        if module_name == "guest":
            template = 'guest_write.html'
        else:
            template = 'write.html'
        return render_to_response(template, data, context_instance = RequestContext(request))

# TODO
# @user_passes_test(lambda u: u.has_perm('document.can_change'))
def view(request, module_name, doc_id=None) :
#     current_page = int(request.GET['current_page'])
#     category_name = module_name
    canonical_module_name = get_canonical_module_name(module_name)
    module_id = get_module_id(canonical_module_name)
#     category = get_category_id(module_name, category_name)
    q = search(request) & Q(module_id=module_id)#  & Q(category=category)

    # if not request.user.is_superuser:
    #     q = q & (Q(is_secret=False) | Q(user=request.user.id))

    category = None

    docs = Document.objects.filter(q).order_by('-is_notice','-id')
    category_name = None
    if request.GET.has_key('category') :
        category = request.GET['category']
        category_name = get_category_name(canonical_module_name, category)
    else: category=1

    docs = docs.filter(category=category)

    page_number = '1'
    if request.GET.has_key('current_page') :
        page_number = request.GET['current_page']

    variables = pagination(request, docs, page_number)

    doc = None
    if doc_id :
        doc = Document.objects.get(id=doc_id)
        doc.hit += 1
        doc.save()

    option_string = get_option_string(request)
    variables.update({'doc' : doc,
                      'module_name':module_name,
                      'option_string':option_string,
                      'category':category,
                      'category_name' : get_category_name(module_name, category)})
#     variables.update({'module_name':category_name})
    return render_to_response(canonical_module_name + '.html', variables,
                              context_instance=RequestContext(request))

## Comment part
@user_passes_test(lambda u: u.has_perm('document.can_add'))
def write_comment(request, doc_id, module_name='') :
    canonical_module_name = get_canonical_module_name(module_name)
    
    doc = Document.objects.get(id=doc_id)
    depth = request.REQUEST.get('depth', 0)

    # if doc.is_secret and not request.user.is_superuser :
    #     return HttpResponseRedirect(get_referer(request))
    
    if request.method == 'POST' :
        form = WriteCommentForm(request.POST)
        if form.is_valid() :
            cmt = Comment(
                user = request.user,
                document = Document.objects.get(id=doc_id),
                content = form.cleaned_data['content'],
                is_secret = form.cleaned_data['is_secret'],
                depth=depth,
                ipaddress = get_ipaddress(request))
            cmt.save()
            if module_name == 'guest':
                return HttpResponseRedirect('/' + module_name + '/')
            else :
                refer = get_referer(request)
                if not refer :
                    refer = '/' + module_name + '/view/' + str(doc.id) + '/?category=' + str(doc.category)
                return HttpResponseRedirect(refer)
    if module_name == 'guest':
        form = GuestWriteCommentForm()
        return render_to_response('guest_comment_write.html', {
            'form':form,
            'user':request.user,
            'doc':doc,
            'module_name':module_name,
            })
    else :
        doc = Document.objects.get(id=doc_id)

        return HttpResponseRedirect('/' + module_name + '/view/' + str(doc.id) + '?category=' + str(doc.category))

# @user_passes_test(lambda u: u.has_perm('comment.can_delete'))
def delete_comment(request, comment_id) :
    cmt = Comment.objects.get(id=comment_id)
    refer = get_referer(request)
    if not refer:
        if request.GET.has_key('refer') :
            refer = request.GET['refer']
        else :
            refer = '/'

    if not request.user.is_superuser :
        if cmt.user :
            if request.user.id != cmt.user.id :
                return HttpResponseRedirect(refer)
        else :
            return HttpResponseRedirect(refer)
        cmt.delete()
        return HttpResponseRedirect(refer) ## REDIRECT TO WHERE?
    else :
        cmt.delete()
        return HttpResponseRedirect(refer) ## REDIRECT TO WHERE?
    return HttpResponse(comment_id)

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def reply_comment(request, doc_id):
    depth = request.REQUEST.get('depth', 0)
    cmt_id = request.REQUEST.get('cmt_id', 0)
    module_name = None

    if request.GET.has_key('module_name'):
        module_name = request.GET['module_name']

    if request.method == 'POST' :
        form = WriteCommentForm(request.POST)
        cmt = None
        if form.is_valid() :
            cmt = Comment(
                user = request.user,
                parent = Comment.objects.get(id=cmt_id),
                content = form.cleaned_data['content'],
                is_secret = form.cleaned_data['is_secret'],
                depth=depth,
                ipaddress = get_ipaddress(request))
            cmt.save()
            if request.POST.has_key('module_name') :
                module_name = request.POST['module_name']
                return HttpResponseRedirect(("/%s/view/%d/#comment_" + str(cmt.id)) % (module_name,int(doc_id)))
            return HttpResponseRedirect(("/blog/view/%d/#comment_" + str(cmt.id)) % int(doc_id))
    else :
        try:
            cmt = Comment.objects.get(id=cmt_id)
        except :
            cmt = None
    if module_name in ['worryboard', 'shop', 'faq', 'notice'] :
        return render_to_response('board_comment_edit_reply.html' ,
                                  {
                                      'cmt':cmt,
                                      'doc_id':doc_id,
                                      'depth':int(depth)+1,
                                      'module_name':module_name,
                                      },
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('blog_comment_edit_reply.html' ,
                                  {
                                      'cmt':cmt,
                                      'doc_id':doc_id,
                                      'depth':int(depth)+1,
                                      'module_name':module_name,
                                      },
                                  context_instance=RequestContext(request))
    

@user_passes_test(lambda u: u.has_perm('document.can_add'))
def edit_comment(request, comment_id, module_name = ''):
    cmt = get_object_or_404(Comment, id=comment_id)
    module_name = None

    if cmt.user :
        if request.user.id != cmt.user.id :
            return HttpResponseRedirect(get_referer(request))
    else :
        if not request.user.is_superuser :
            return HttpResponseRedirect(get_referer(request))

    if request.GET.has_key('module_name'):
        module_name = request.GET['module_name']

    if request.method == 'POST' :
        if cmt.document :
            doc_id = cmt.document.id
        else :
            doc_id = cmt.parent.document.id

        form = WriteCommentForm(request.POST)
        if form.is_valid() :
            cmt.content = form.cleaned_data['content']
            cmt.is_secret = form.cleaned_data['is_secret']
            cmt.save()

        if request.GET.has_key('module_name'):
            module_name = request.GET['module_name']
            if module_name == 'guest':
                return HttpResponseRedirect("/guest/")
            else :
                return HttpResponseRedirect("/blog/view/%d/#comment_%d" % (doc_id, cmt.id))
        elif request.POST.has_key('module_name') :
            module_name = request.POST['module_name']
            return HttpResponseRedirect("/%s/view/%d/%s" % (module_name, doc_id, get_option_string(request)))
        else:
            return HttpResponseRedirect("/blog/view/%d/#comment_%d" % (doc_id, cmt.id))
        
    else :
        if module_name in ['shop','faq','notice','worryboard'] :
            return render_to_response('board_comment_edit_reply.html' ,
                                      {
                                          'edit': True,
                                          'cmt':cmt,
                                          'module_name':module_name,
                                          },
                                      context_instance=RequestContext(request))
        else :
            return render_to_response('blog_comment_edit_reply.html' ,
                                      {
                                          'edit': True,
                                          'cmt':cmt,
                                          'module_name':module_name,
                                          },
                                      context_instance=RequestContext(request))


if __name__ == '__main__' :
	import settings
	print 'hello'
