#!/bin/sh
# taken from: mbrownnycnyc/nsclient_update.sh
# (https://gist.github.com/mbrownnycnyc/5644413/revisions)
ADDR=`/sbin/ifconfig eth0 | grep 'inet addr' | awk '{print $2}' | sed -e s/.*://`
HOST=`hostname`
echo "update delete $HOST A" > /var/nsupdate.txt
echo "update add $HOST 86400 A $ADDR" >> /var/nsupdate.txt
echo "update delete $HOST PTR" > /var/nsupdate.txt
echo "update add $HOST 86400 PTR $ADDR" >> /var/nsupdate.txt
nsupdate /var/nsupdate.txt
