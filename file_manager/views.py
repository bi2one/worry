# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from worry.file_manager.models import File

from xml.etree import ElementTree
import datetime
import base64

from worry.document.models import Document, Comment, Tag
from django.contrib.auth.models import User, Group

from PIL import Image

def get_date(ss) :
    year = ss[:4]
    month = ss[4:6]
    day = ss[6:8]
    hour = ss[8:10]
    min = ss[10:12]
    sec = ss[12:14]

    return "%s-%s-%s %s:%s:%s" % (year, month, day, hour, min, sec)

def handle_image(i) :
    resize_size = settings.RESIZE_SIZE
    thumb_size = settings.THUMB_SIZE

    im = Image.open(settings.UPLOAD_DIR + str(i))

    thumb_size = thumb_size, thumb_size
    width = im.size[0] * 1.0
    height = im.size[1] * 1.0

    ratio = height / width

    if width > resize_size :
        new_width = resize_size
        new_height = new_width * ratio
    else :
        new_width = width;
        new_height = height;

    new = im.resize((new_width, new_height))
    new.save(settings.UPLOAD_DIR + str(i) + "_resized", "PNG")

    im.thumbnail(thumb_size, Image.ANTIALIAS)
    im.save(settings.UPLOAD_DIR + str(i) + "_thumb", "PNG")

    image_query = "?type=2&"
    imageurl = "/file/" + str(i) + image_query + "size=3"
    originalurl = "/file/" + str(i) + image_query + "size=1"
    thumburl = "/file/" + str(i) + image_query + "size=2"
    return {'imageurl' : imageurl, 'originalurl' : originalurl, 'thumburl' : thumburl}

def serve_file(request, file_id=None):
    f = get_object_or_404(File, pk=file_id)
    f_path = settings.UPLOAD_DIR + str(file_id)

    serve_type = int(request.GET['type'])
    if request.GET.has_key('size') :
        image_type = int(request.GET['size'])
    
    response=None
    if serve_type == 1 :
        response = HttpResponse(open(f_path), mimetype=f.mime_type)
        response['Content-Disposition'] = 'attachment; filename=' + f.file_name
    elif serve_type == 2 :
        if image_type == 1 : # original
            response = HttpResponse(open(f_path), mimetype=f.mime_type)
        elif image_type == 2 : # thumb
            f_path += "_thumb"
            response = HttpResponse(open(f_path), mimetype=f.mime_type)
            # response['Content-Length'] = os.path.size(f_path)
        elif image_type == 3 : # resized
            f_path += "_resized"
            response = HttpResponse(open(f_path), mimetype=f.mime_type)
            # response['Content-Length'] = os.path.size(f_path)

    return response


def upload(request):
    if request.POST['type'] == 'file' :
        f = request.FILES['file']
        file_mime = f.content_type
        file_name = f.name
        file_size = f.size

        file_id = handle_upload_file(f)
        file_url = "/file/" + str(file_id) + "?type=1"

        return render_to_response('uploaded.html', {'file_url' : file_url,
                                                    'file_mime' : file_mime,
                                                    'file_name' : file_name,
                                                    'file_size' : file_size,
                                                    'file_id' : file_id})
    else :
        f = request.FILES['file']
        file_mime = f.content_type
        file_name = f.name
        file_size = f.size
        file_id = handle_upload_file(f)
        url_info = handle_image(file_id)

        return render_to_response('uploaded_image.html', {'imageurl' : url_info['imageurl'],
                                                          'originalurl' : url_info['originalurl'],
                                                          'thumburl' : url_info['thumburl'],
                                                          'filename' : file_name,
                                                          'filesize' : file_size,
                                                          'file_id' : file_id})
def handle_upload_file(f) :
    new_f = File(file_type=0, mime_type = f.content_type, file_name = f.name, file_size=f.size)
    new_f.save()

    destination = open(settings.UPLOAD_DIR + str(new_f.pk), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return new_f.pk

def deco(input) :
    return base64.decodestring(input)

def mig(request) :
    file_name = "/home/worry/migration/blog.xml"
    t = ElementTree
    tree = t.parse(file_name)
    root = tree.getroot()
    posts = root.getiterator("post")

    for post in posts :
        title = post.find("title").text
        try:
            username = post.find("user_id").text
            user = User.objects.get(username=username)
        except Exception,e:
            user = None
        nick_name = post.find("nick_name").text
        password = post.find("password").text
        pub_date = post.find("regdate").text
        ipaddress = post.find("ipaddress").text
        is_secret = str(post.find("is_secret").text) == 'Y'
        try:
            hit = post.find("readed_count").text
        except:
            hit = 0
        content = post.find("content").text
        doc = Document(module_id=1, 
                       user=user,
                       module_name="blog",
                       category=2,
                       category_name='worry',
                       is_secret=is_secret,
                       title=title,
                       content=content,
                       ipaddress =ipaddress,
                       username=username,
                       hit=hit,
                       pub_date = pub_date)
        doc.save()
        doc.pub_date=get_date(post.find('regdate').text)
        tag_name = "걱정인형"
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        doc.tag_set.add(tag)
        doc.save()

        try :
            comments = post.find("comments").getiterator("comment")
        except :
            comments = []

        for comment in comments :
            try :
                cmt = comment.find("password").text
            except:
                cmt = None
            is_secret = (str(comment.find("is_secret").text) == 'Y')

            
            username = comment.find("user_id")
            if not username :
                username = comment.find("nick_name")
                if not username  :
                    username = 'None'
                else :
                    username = username.text
            else :
                username = username.text

            try :
                user = User.objects.get(username=username)
            except :
                user=None

            cmt = Comment(document=doc, 
                          user=user,
                          is_secret=is_secret,
                          content=comment.find("content").text,
                          ipaddress=comment.find("ipaddress").text,
                          username=comment.find("nick_name").text,
                          password=cmt)
            cmt.save()
            cmt.pub_date = get_date(comment.find("regdate").text)
            cmt.save()
        
    return HttpResponse('good')

def serve_img(request, path) :
    return HttpResponse(path)


def mig_shop(request) :
    docs = Document.objects.filter(category=2)
    for doc in docs :
        doc.delete()

    file_name = "/home/worry/migration/shop.xml"
    t = ElementTree
    tree = t.parse(file_name)
    root = tree.getroot()
    posts = root.getiterator("post")

    for post in posts :
        title = deco(post.find("title").text)
        nick_name = deco(post.find("nick_name").text)

        try:
            username = deco(post.find("user_id").text)
            user = User.objects.get(username=username)
        except Exception,e:
            user = None
            username = nick_name

        password = deco(post.find("password").text)
        pub_date = deco(post.find("regdate").text)
        ipaddress = deco(post.find("ipaddress").text)
        is_secret = str(deco(post.find("is_secret").text)) == 'Y'
        try:
            hit = deco(post.find("readed_count").text)
        except:
            hit = 0
        content = deco(post.find("content").text)

        try :
            if str(deco(post.find("notify_message").text)) == 'Y':
                category=3
                category_name="notice"
            else :
                category=2
                category_name="shop"
        except :
            category=2
            category_name="shop"

        doc = Document(module_id=2,
                       user=user,
                       username=username,
                       module_name="board", 
                       category=category,
                       category_name=category_name,
                       is_secret=is_secret,
                       title=title,
                       content=content,
                       ipaddress =ipaddress,
                       hit=hit,
                       pub_date = pub_date)
        doc.save()
        doc.pub_date=get_date(deco(post.find('regdate').text))
        doc.save()

        try :
            comments = post.find("comments").getiterator("comment")
        except :
            comments = []

        for comment in comments :
            try :
                cmt = deco(comment.find("password").text)
            except:
                cmt = None
            is_secret = str(deco(comment.find("is_secret").text)) == 'Y'

            username = comment.find("user_id")

            if not username :
                username = comment.find("nick_name")
                if not username :
                    user = None
                else :
                    username = deco(username.text)
            else : 
                username = deco(username.text)

            try :
                user = User.objects.get(username=username)
            except :
                user = None
            cmt = Comment(document=doc, 
                          user=user,
                          is_secret=is_secret,
                          content=deco(comment.find("content").text),
                          ipaddress=deco(comment.find("ipaddress").text),
                          username=deco(comment.find("nick_name").text),
                          password=cmt)
            cmt.save()
            cmt.pub_date = get_date(deco(comment.find("regdate").text))
            cmt.save()
        
    return HttpResponse('good')





def mig_qna(request) :
    docs = Document.objects.filter(category=4)
    for doc in docs :
        doc.delete()

    file_name = "/home/worry/migration/qna.xml"
    t = ElementTree
    tree = t.parse(file_name)
    root = tree.getroot()
    posts = root.getiterator("post")

    for post in posts :
        title = deco(post.find("title").text)
        try:
            username = deco(post.find("user_id").text)
            user = User.objects.get(username=username)
        except Exception,e:
            user = None
        nick_name = deco(post.find("nick_name").text)
        password = deco(post.find("password").text)
        pub_date = deco(post.find("regdate").text)
        ipaddress = deco(post.find("ipaddress").text)
        is_secret = str(deco(post.find("is_secret").text)) == 'Y'

        if is_secret :
            continue;
        try:
            hit = deco(post.find("readed_count").text)
        except:
            hit = 0
        content = deco(post.find("content").text)

        try :
            if str(deco(post.find("notify_message").text)) == 'Y':
                continue;
            else :
                category=4
                category_name="faq"
        except:
                category=4
                category_name="faq"


        doc = Document(module_id=2,
                       user=user,
                       module_name="board", 
                       category=category,
                       category_name=category_name,
                       is_secret=is_secret,
                       title=title,
                       content=content,
                       ipaddress =ipaddress,
                       hit=hit,
                       pub_date = pub_date)
        doc.save()
        doc.pub_date=get_date(deco(post.find('regdate').text))
        doc.save()

        try :
            comments = post.find("comments").getiterator("comment")
        except :
            comments = []

        for comment in comments :
            try :
                cmt = deco(comment.find("password").text)
            except:
                cmt = None
            is_secret = str(deco(comment.find("is_secret").text)) == 'Y'

            
            username = comment.find("user_id")
            if not username :
                username = comment.find("nick_name")
                if not username :
                    username = None
                else : username = deco(username.text)
            else : username = deco(username.text)

            try :
                user = User.objects.get(username=username)
            except :
                user = None

            cmt = Comment(document=doc, 
                          user=user,
                          is_secret=is_secret,
                          content=deco(comment.find("content").text),
                          ipaddress=deco(comment.find("ipaddress").text),
                          username=deco(comment.find("nick_name").text),
                          password=cmt)
            cmt.save()
            cmt.pub_date = get_date(deco(comment.find("regdate").text))
            cmt.save()
        
    return HttpResponse('good')

def mig_worry(request) :
    docs = Document.objects.filter(category=1)
    for doc in docs :
        doc.delete()

    file_name = "/home/worry/migration/worry.xml"
    t = ElementTree
    tree = t.parse(file_name)
    root = tree.getroot()
    posts = root.getiterator("post")

    for post in posts :
        title = deco(post.find("title").text)

        nick_name = deco(post.find("nick_name").text)

        try:
            username = deco(post.find("user_id").text)
            user = User.objects.get(username=username)
        except Exception,e:
            user = None
            username = nick_name

        password = deco(post.find("password").text)
        pub_date = deco(post.find("regdate").text)
        ipaddress = deco(post.find("ipaddress").text)
        is_secret = str(deco(post.find("is_secret").text)) == 'Y'
        try:
            hit = deco(post.find("readed_count").text)
        except:
            hit = 0
        content = deco(post.find("content").text)

        try :
            if str(deco(post.find("notify_message").text)) == 'Y':
                category=3
                category_name="notice"
            else :
                category=1
                category_name="worryboard"
        except :
            category=1
            category_name="worryboard"

        doc = Document(module_id=2,
                       user=user,
                       username=username,
                       module_name="board", 
                       category=category,
                       category_name=category_name,
                       is_secret=is_secret,
                       title=title,
                       content=content,
                       ipaddress =ipaddress,
                       hit=hit,
                       pub_date = pub_date)
        doc.save()
        doc.pub_date=get_date(deco(post.find('regdate').text))
        doc.save()

        try :
            comments = post.find("comments").getiterator("comment")
        except :
            comments = []

        for comment in comments :
            try :
                cmt = deco(comment.find("password").text)
            except:
                cmt = None
            is_secret = str(deco(comment.find("is_secret").text)) == 'Y'

            username = comment.find("user_id")

            if not username :
                username = comment.find("user_id")
                if not username :
                    username = None
                else : username = deco(username.text)
            else : username = deco(username.text)

            try :
                user = User.objects.get(username=username)
            except :
                user = None


            cmt = Comment(document=doc, 
                          user=user,
                          is_secret=is_secret,
                          content=deco(comment.find("content").text),
                          ipaddress=deco(comment.find("ipaddress").text),
                          username=deco(comment.find("nick_name").text),
                          password=cmt)
            cmt.save()
            cmt.pub_date = get_date(deco(comment.find("regdate").text))
            cmt.save()
        
    return HttpResponse('good')




def mem(request) :
    file_name = "/home/worry/migration/member.xml"
    t = ElementTree
    tree = t.parse(file_name)
    root = tree.getroot()
    members = root.getiterator("member")

    group = Group.objects.get(name="auth_user")
    for member in members :
        username = deco(member.find("user_id").text)
        nick_name = deco(member.find("nick_name").text)
        password = deco(member.find("password").text)
        try:
            email = deco(member.find("email").text)
        except:
            email = ''
        regdate = deco(member.find("regdate").text)
        u = User(username=username, nick_name=nick_name,
                 password=password, email=email)
        u.save()
        u.groups.add(group)
        u.date_joined = get_date(regdate)
        u.save()

    return HttpResponse('good')


#         content = article.find("content").text.replace('lambda','<br />')
#         post = Post(notice=0,username=username,password=password,title=title,body=content,hit=0,boom_up=0,boom_down=0,score=0)
#         post.save()
#         post.pub_date=datetime.datetime(pub_date[0],pub_date[1],pub_date[2])
#         post.save()
#         items = article.find("comments").getiterator("item")
#         for item in items :
#             username = item.find("username").text
#             pub_date = map(lambda x:int(x),item.find("datetime").text.split('-'))
#             body = item.find("body").text.replace('lambda','<br />')
#             password = hashlib.md5('vatechgirls'.encode('utf-8')).hexdigest()
#             comment = Comment(post=post,username=username,password=password,body=body,boom_up=0)
#             comment.save()
#             comment.pub_date=datetime.datetime(pub_date[0],pub_date[1],pub_date[2])
#             comment.save()
#     return HttpResponse("success")
