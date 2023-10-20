#!/bin/sh

#EXTERNALIP=`external-ip`
NAMESERVER=ns1.holmnet.dk
DOMAIN=int.holmnet.dk
WEBSERVER=http://www.holmnet.dk/myip.php
HOSTNAME=`hostname`
DNSNAME=$HOSTNAME.int.holmnet.dk
TTL=600
CURRENTIP=`dig +short $DNSNAME`

EXTERNALIP=`wget -q -O - $WEBSERVER`


nsupdate <<STOP
server $NAMESERVER
zone $DOMAIN
update delete $DNSNAME  A 
send
update add $DNSNAME $TTL A $EXTERNALIP
send
STOP

#echo Old IP $CURRENTIP
#echo New IP $EXTERNALIP

if [ "$CURRENTIP" != "$EXTERNALIP" ]
then
echo $CURRENTIP new $EXTERNALIP |  mail -s "Mailadresse er skiftet til $EXTERNALIP " peter@l-holm.dk 

fi
