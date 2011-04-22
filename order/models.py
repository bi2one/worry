# order
from django.contrib.auth.models import User
from django.db import models

class Bank(models.Model) :
    def __unicode__(self) :
        return self.name + " _ " + self.depositor_name

    name = models.CharField(max_length=45)
    number = models.CharField(max_length=255)
    depositor_name = models.CharField(max_length=45)

class Order(models.Model) :
    def __unicode__(self) :
        return self.content

    user = models.ForeignKey(User, null=True)
    bank = models.ForeignKey(Bank, null=True)

    sender_name = models.CharField(max_length=45)
    sender_phone = models.CharField(max_length=45)
    
    doll_count = models.PositiveIntegerField(default=0)
    phonedoll_count = models.PositiveIntegerField(default=0)

    content = models.TextField()

    payment_name = models.CharField(max_length=45, null=False)
    receiver_name = models.CharField(max_length=45, null=False)
    receiver_phone = models.CharField(max_length=45, null=True)
    receiver_address = models.CharField(max_length=255, null=False)
    receiver_address_number = models.CharField(max_length=45, null=False)

    send_issue = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    
    state = models.CharField(max_length=1,
                             choices=((0, 'before_payment'),
                                      (1, 'create'),
                                      (2, 'send'),
                                      (3, 'done'),
                                      (4, 'fail')))

