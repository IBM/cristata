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

TS=Cristata-TimeSeriesRetrieve
ADD=Cristata-TimeSeriesInsert
DEV=Cristata-DeviceListing

ACTION=create
EXISTS=$(bx wsk action list | grep $TS)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION --kind python:3 $DB2_PARAMS --param database $DB2_SCHEMA.GET_TS --param debug true $TS $DIR/get_ts-$DBVERSION.zip

ACTION=create
EXISTS=$(bx wsk action list | grep $ADD)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION --kind python:3 $DB2_PARAMS --param database $DB2_SCHEMA.ADD_TS --param debug true $ADD $DIR/insert-$DBVERSION.zip

ACTION=create
EXISTS=$(bx wsk action list | grep $DEV)
if [ -n "$EXISTS" ]; then
	ACTION=update
fi
bx wsk action $ACTION --kind python:3 $DB2_PARAMS --param database $DB2_SCHEMA.GET_DEVICES --param debug true $DEV $DIR/get_devices-$DBVERSION.zip

bx wsk package refresh

feed="Bluemix_cristata-mhub_credentials/messageHubFeed"
bx wsk trigger create cristata-mhub-$DBVERSION --feed $feed --param topic watson-iot
bx wsk rule create cristata-mhub-rule-$DBVERSION cristata-mhub-$DBVERSION $ADD

