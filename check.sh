#!/bin/sh

mysql -u dontworry -p dontworry -e "select count(*) from document_document where pub_date > '2011-01-04%' and category=2" --password=worryworry
mysql -u dontworry -p dontworry -e "select count(*) from auth_user date_joined where date_joined > '2011-01-04%' order by date_joined desc;" --password=worryworry
