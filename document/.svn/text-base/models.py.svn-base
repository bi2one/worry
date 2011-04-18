# document
from django.contrib.auth.models import User
from django.db import models

class Document(models.Model) :
    def __unicode__(self) :
        return self.title +" _ "+self.module_name

    class Meta:
        permissions = (
            ("can_add", "Can add document"),
            ("can_delete", "Can delete document"),
            ("can_change", "Can change document"),
        )

    user = models.ForeignKey(User, null=True)

    module_id = models.PositiveSmallIntegerField()
    module_name = models.CharField(max_length=255)

    category = models.PositiveSmallIntegerField(null=True)
    category_name = models.CharField(max_length=255, null=True)

    is_notice = models.BooleanField(default=False)

    title = models.CharField(max_length=255)
    content = models.TextField()
    hit = models.PositiveIntegerField()
    is_secret = models.BooleanField(default=False)
    ipaddress = models.CharField(max_length=50)
    pub_date = models.DateTimeField(auto_now_add=True)

    # for guest
    username = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=128, null=True)

class Comment(models.Model) :
    def __unicode__(self) :
        return self.content

    class Meta:
        permissions = (
            ("can_add", "Can add comment"),
            ("can_delete", "Can delete comment"),
            ("can_change", "Can change comment"),
        )

    user = models.ForeignKey(User, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    depth = models.PositiveIntegerField(default=0)

    document = models.ForeignKey(Document, null=True)
    content = models.TextField()
    is_secret = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    ipaddress = models.CharField(max_length=50)

    # for guest
    username = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=128, null=True)

class Tag(models.Model) :
    def __unicode__(self) :
        return self.name
    name = models.CharField(max_length=64, unique=True)
    documents = models.ManyToManyField(Document)
    count = models.PositiveIntegerField(default=0)

