#!/bin/sh

# dontworry.order_bank initial data
python manage.py loaddata fixtures/order_bank.json
python manage.py dumpdata order.bank
# dontworry.order_address initial data
python load_address_data.py fixtures/20110501_address_number.csv