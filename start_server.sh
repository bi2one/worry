#!/bin/bash

# Replace these three settings.
PROJDIR="/Users/bi2one/public_html/worry"
PIDFILE="$PROJDIR/worry.pid"
SOCKET="$PROJDIR/worry.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

/usr/bin/env - \
PYTHONPATH="../python:.." \
python manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE
chmod 777 ./worry.sock
