#!/bin/bash
#Author: Mark Purcell
#Cloud Service Names

prefix=cristata

export CRISTATA_DB2=$prefix-db2
export CREDENTIAL_DB2=credentials
export CRISTATA_IOT=$prefix-iot
export CREDENTIAL_IOT=credentials
export CRISTATA_MHUB=$prefix-mhub
export CREDENTIAL_MHUB=credentials
export TOPIC_MHUB=watson-iot

#IBM Cloud Functions definitions
export CRISTATA_WSK_TRIGGER=$prefix-mhub-
export CRISTATA_WSK_RULE=$prefix-mhub-rule-
export WSK_TS=$prefix-TimeSeriesRetrieve
export WSK_ADD=$prefix-TimeSeriesInsert
export WSK_DEV=$prefix-DeviceListing

export WSK_FEED='Bluemix_'$CRISTATA_MHUB'_'$CREDENTIAL_MHUB'/messageHubFeed'

