# -*- coding: utf-8 -*-

import sys, settings

if len(sys.argv) != 2 :
    print "usage: python load_address_data.py [csv address data file for dump]"
    exit(0);

from django.core.management import setup_environ
setup_environ(settings)
from order.models import Address

filename = sys.argv[1]

f = open(filename, 'r')

Address.objects.all().delete()
for raw_field in f.readlines():
    field = raw_field.split(',')
    cleared_field = map((lambda x: x.replace("\n","").replace("\r","").strip()), field)

    addr = Address(
        ZIPCODE = cleared_field[0],
        SIDO = cleared_field[1],
        GUGUN = cleared_field[2],
        DONG = cleared_field[3],
        RI = cleared_field[4],
        BLDG = cleared_field[5],
        BUNJI = cleared_field[6],
        SEQ = cleared_field[7]
        )
    addr.save()
