#!/bin/bash
#Author: Mark Purcell (markpurcell@ie.ibm.com)

if [[ ! $# -eq 1 ]] ; then
	echo "Usage: Bluemix space (e.g. dev)"
        exit 0
fi

if [[ ! -f my_setup.sh ]]; then
	echo "Must run provision.sh first " $1
	exit 1
fi

source my_setup.sh
source ../service_names.sh

DIR=.
DBVERSION=$(cat $DIR/VERSION)

if [[ ! -f $DIR/get_ts-$DBVERSION.zip ]]; then
	echo "Must run make build first " $1
	exit 1
fi
if [[ ! -f $DIR/insert-$DBVERSION.zip ]]; then
	echo "Must run make build first " $1
	exit 1
fi
if [[ ! -f $DIR/get_devices-$DBVERSION.zip ]]; then
	echo "Must run make build first " $1
	exit 1
fi

ACTION=create
EXISTS=$(bx wsk action list | grep $WSK_TS)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION --kind python:3 $DB2_PARAMS --param database $DB2_SCHEMA.GET_TS --param debug true $WSK_TS $DIR/get_ts-$DBVERSION.zip

ACTION=create
EXISTS=$(bx wsk action list | grep $WSK_ADD)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION --kind python:3 $DB2_PARAMS --param database $DB2_SCHEMA.ADD_TS --param debug true $WSK_ADD $DIR/insert-$DBVERSION.zip

ACTION=create
EXISTS=$(bx wsk action list | grep $WSK_DEV)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION --kind python:3 $DB2_PARAMS --param database $DB2_SCHEMA.GET_DEVICES --param debug true $WSK_DEV $DIR/get_devices-$DBVERSION.zip

bx wsk package refresh

temp=`bx wsk trigger list | grep $CRISTATA_WSK_TRIGGER | cut -d'/' -f3 | cut -d' ' -f1`
if [ -n "$temp" ]; then
    bx wsk trigger delete $temp
fi

temp=`bx wsk rule list | grep $CRISTATA_WSK_RULE | cut -d'/' -f3 | cut -d' ' -f1`
if [ -n "$temp" ]; then
    bx wsk rule delete $temp
fi

bx wsk trigger create $CRISTATA_WSK_TRIGGER$DBVERSION --feed $WSK_FEED --param topic $TOPIC_MHUB
bx wsk rule create $CRISTATA_WSK_RULE$DBVERSION $CRISTATA_WSK_TRIGGER$DBVERSION $WSK_ADD

