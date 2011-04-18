from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from worry.twitter.worry_oauth import *
from django.template import RequestContext
from worry.document.models import Document
# from django.utils.encoding import smart_str

from worry.twitter.models import *

# for bitly
import worry.twitter.bitly.bitly as bitly
from django.conf import settings

# bitly
bitly_api = bitly.Api(login=settings.BITLY_LOGIN ,apikey=settings.BITLY_APIKEY)

# twitter access_token
access_token = oauth.OAuthToken.from_string(settings.TWITTER_ACCESS_TOKEN_STRING)

import json
import re

def save_tweet(document) :
    tweet = Tweet(document=document)
    tweet.save()

def get_module_name(doc) :
    if doc.category_name in settings.BLOG_CATEGORY_ID.keys() :
        return 'blog'
    elif doc.category_name in settings.BOARD_CATEGORY_ID.keys() :
        return doc.category_name
    elif doc.module_name == 'guest' :
        return 'guest'
    else :
        return False

def get_140_string(doc) :
    module_name = get_module_name(doc)
    if module_name not in settings.MODULE_NAMES :
        return None
    if module_name in settings.MODULE_NAMES[5:] :
        original_url = 'dontworryworry.com/?next=/guest'
    else :
        original_url = 'dontworryworry.com/?next='+doc.category_name+'/view/'+str(doc.id)+'/?category='+str(doc.category)
    shorten_url = bitly_api.shorten(original_url)
    url_hashtag = ' ... ' + shorten_url + ' #worry'

    long_status = None
    if module_name in settings.MODULE_NAMES[:5] :
        long_status = doc.title
    else :
        long_status = doc.content
    length = 140 - len(url_hashtag)
    status = long_status[:length]
    # status = smart_str(status)
    status += url_hashtag
    status = status.encode('utf-8')
    return status

def twit_to_twitter() :
    if is_authenticated(access_token) :
        tweets = Tweet.objects.all()[:10] # how many for one time?
        for tweet in tweets :
            status = get_140_string(tweet.document)
            success = update_status(access_token, status)
            if success :                    # success case 
                sended=True
            else :                          # fail case
                sended=False
            log = TweetLog(document=tweet.document,sended=sended)
            tweet.delete()
            log.save()

def get_and_save_mentions(since_id, page) :
    mentions = get_mentions(access_token, since_id, page, 200)
    if mentions :
        if len(json.loads(mentions)) == 200 :
            get_and_save_mentions(page+1, since_id)
        mentions = json.loads(mentions)
        mentions.reverse()
        for mention in mentions :
            m = re.match('^#worry$|^#worry .*$|^.* #worry .*$|^.* #worry$', mention['text'])
            content = mention['text']
            term = re.search(' *#worry *', content)
            if term :
                content = content.replace(term.group(), ' ')
            term = re.search(' *@dontworrycenter *', content)
            if term :
                content = content.replace(term.group(), ' ')
            content = content.strip()
            if m :
                doc = Document(
                    module_id=2,
                    module_name='board',
                    category=1,
                    category_name='worryboard',
                    title=content[:20]+' ...',
                    content=content,
                    hit=0,
                    ipaddress=mention['id'],
                    username=mention['user']['screen_name']
                    )
                doc.save()
            else :
                doc = Document(
                    module_id=3,
                    module_name='guest',
                    content=content,
                    hit=0,
                    ipaddress=mention['id'],
                    username=mention['user']['screen_name']
                    )
                doc.save()
            last_id = mention['id']
        return last_id

def post_from_twitter() :
    if is_authenticated(access_token) :
        FILE = open('/home/worry/worry/twitter/last_timeline_id', 'r')
        since_id = int(FILE.read())
        FILE.close()
        last_id = get_and_save_mentions(since_id, 1)
        if last_id :
            FILE = open('/home/worry/worry/twitter/last_timeline_id', 'w')
            FILE.write(str(last_id))
            FILE.close()
