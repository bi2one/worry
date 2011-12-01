#!/bin/bash

# Replace these three settings.
PROJDIR="/home/worry/worry"
#PROJDIR="/home/worry/worry_test/worry/"
PIDFILE="$PROJDIR/worry.pid"
SOCKET="$PROJDIR/worry.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

/usr/bin/env - \
PYTHONPATH="../python:.." \
python manage.py runfcgi protocol=scgi host=127.0.0.1 port=28406 pidfile=$PIDFILE
chmod 777 ./worry.sock
