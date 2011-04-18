# twitter
from worry.twitter.worry_oauth import *
import oauth.oauth as oauth

from django.db import models
from worry.document.models import Document

class Tweet(models.Model) :
    document = models.ForeignKey(Document)

class TweetLog(models.Model) :
    document = models.ForeignKey(Document)
    sended = models.BooleanField()
