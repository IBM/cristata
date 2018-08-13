#!/bin/bash
#Author: Mark Purcell (markpurcell@ie.ibm.com)


if [[ ! -f my_setup.sh ]]; then
	echo "Must run provision.sh first "
	exit 1
fi

source my_setup.sh
source ../service_names.sh

DIR=.
DBVERSION=$(cat $DIR/VERSION)

if [[ ! -f $DIR/get_ts-$DBVERSION.zip ]]; then
	echo "Must run make build first "
	exit 1
fi
if [[ ! -f $DIR/get_devices-$DBVERSION.zip ]]; then
	echo "Must run make build first "
	exit 1
fi
if [[ ! -f $DIR/db2-insert-$DBVERSION.zip ]]; then
	echo "Must run make build first "
	exit 1
fi
if [[ ! -f $DIR/mhub-parse-$DBVERSION.zip ]]; then
	echo "Must run make build first "
	exit 1
fi

# create/update get timeseries action
ACTION=create
EXISTS=$(bx wsk action list | grep $WSK_TS)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION --kind python:3 $DB2_PARAMS --param database $DB2_SCHEMA.GET_TS --param debug true $WSK_TS $DIR/get_ts-$DBVERSION.zip

# create/update get devices action
ACTION=create
EXISTS=$(bx wsk action list | grep $WSK_DEV)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION --kind python:3 $DB2_PARAMS --param database $DB2_SCHEMA.GET_DEVICES --param debug true $WSK_DEV $DIR/get_devices-$DBVERSION.zip

# create/update message hub parse action
ACTION=create
EXISTS=$(bx wsk action list | grep $WSK_ADD)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION  --kind python:3  $WSK_MHUB $DIR/mhub-parse-$DBVERSION.zip

# create/update timeseries insert action
ACTION=create
EXISTS=$(bx wsk action list | grep $WSK_ADD)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION  --kind python:3  $DB2_PARAMS  --param database $DB2_SCHEMA.ADD_TS  --param debug true  $WSK_TSINSERT $DIR/db2-insert-$DBVERSION.zip

# create/update insert sequence
ACTION=create
EXISTS=$(bx wsk action list | grep $WSK_ADD)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action create $WSK_INSERT  --sequence $WSK_MHUB,$WSK_TSINSERT

bx wsk package refresh

temp=`bx wsk trigger list | grep $CRISTATA_WSK_TRIGGER | cut -d'/' -f3 | cut -d' ' -f1`
if [ -n "$temp" ]; then
    bx wsk trigger delete $temp
fi

temp=`bx wsk rule list | grep $CRISTATA_WSK_RULE | cut -d'/' -f3 | cut -d' ' -f1`
if [ -n "$temp" ]; then
    bx wsk rule delete $temp
fi

increment=$RANDOM
bx wsk trigger create $CRISTATA_WSK_TRIGGER$increment --feed $WSK_FEED --param topic $TOPIC_MHUB
bx wsk rule create $CRISTATA_WSK_RULE$increment $CRISTATA_WSK_TRIGGER$increment $WSK_INSERT
