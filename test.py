import datetime
target = datetime.datetime(year=2011,month=7,day=1)
target = datetime.datetime(year=2011,month=1,day=1)
target2 = datetime.datetime(year=2011,month=1,day=30)
User.objects.filter(date_joined__gt = target).filter(date_joined__lt = target2).count()
