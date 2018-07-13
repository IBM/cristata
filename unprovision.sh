#!/bin/bash
#Author: Mark Purcell

source ./service_names.sh

#First remove wsk triggers/rules
temp=`bx wsk trigger list | grep $CRISTATA_WSK_TRIGGER | cut -d'/' -f3 | cut -d' ' -f1`
if [ -n "$temp" ]; then
    bx wsk trigger delete $temp
fi

temp=`bx wsk rule list | grep $CRISTATA_WSK_RULE | cut -d'/' -f3 | cut -d' ' -f1`
if [ -n "$temp" ]; then
    bx wsk rule delete $temp
fi

bx service key-delete -f $CRISTATA_MHUB $CREDENTIAL_MHUB

#MHub can have IoT keys which must be removed
temp=`bx service keys $CRISTATA_MHUB | sed -e '1,5d'`
if [ -n "$temp" ]; then
    bx service key-delete -f $CRISTATA_MHUB $temp
fi

bx service delete -f $CRISTATA_MHUB

#Now remove the IoT platform
bx service key-delete -f $CRISTATA_IOT $CREDENTIAL_IOT
bx service delete -f $CRISTATA_IOT

#And then DB2
bx service key-delete -f $CRISTATA_DB2 $CREDENTIAL_DB2
bx service delete -f $CRISTATA_DB2


