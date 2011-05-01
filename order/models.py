# order
from django.contrib.auth.models import User
from django.db import models

class Bank(models.Model) :
    def __unicode__(self) :
        return self.name + " _ " + self.depositor_name

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    depositor_name = models.CharField(max_length=255)

class Order(models.Model) :
    def __unicode__(self) :
        return self.content

    user = models.ForeignKey(User, null=True)
    bank = models.ForeignKey(Bank, null=True)

    sender_name = models.CharField(max_length=255)
    sender_phone = models.CharField(max_length=255)
    
    doll_count = models.PositiveIntegerField(default=0)
    phonedoll_count = models.PositiveIntegerField(default=0)

    content = models.TextField()

    payment_name = models.CharField(max_length=255, null=False)
    receiver_name = models.CharField(max_length=255, null=False)
    receiver_phone = models.CharField(max_length=255, null=True)
    receiver_address = models.CharField(max_length=255, null=False)
    receiver_address_number = models.CharField(max_length=255, null=False)

    send_issue = models.TextField(null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    state = models.CharField(max_length=255,
                             choices=((0, 'before_payment'),
                                      (1, 'create'),
                                      (2, 'send'),
                                      (3, 'done'),
                                      (4, 'fail')))

class Address(models.Model) :
    def __unicode__(self) :
        return self.ZIPCODE

    ZIPCODE = models.CharField(max_length="14", null=True)
    SIDO = models.CharField(max_length="8", null=True)
    GUGUN = models.CharField(max_length="34", null=True)
    DONG = models.CharField(max_length="52", null=True)
    RI = models.CharField(max_length="36", null=True)
    BLDG = models.CharField(max_length="80", null=True)
    BUNJI = models.CharField(max_length="34", null=True)
    SEQ = models.CharField(max_length="10", null=True)
