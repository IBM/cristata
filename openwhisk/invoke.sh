#!/bin/bash
#Author: Mark Purcell (markpurcell@ie.ibm.com)
#This script shows how to invoke an action via REST

source ../service_names.sh

#Lets grab some OW properties first
ow_key=`bx wsk property get --auth | tr -s "\t" | cut -f2`
ow_host=`bx wsk property get --apihost | tr -s "\t" | cut -f2`
ow_ver=`bx wsk property get --apiversion | tr -s "\t" | cut -f2`
ow_url="https://$ow_host/api/$ow_ver/namespaces"
ow_space=`bx wsk action list | grep $WSK_ADD | cut -f1 -d' ' | cut -f2 -d'/'`

curl -u $ow_key --header "Content-Type: application/json" -X POST $ow_url/$ow_space/actions/$WSK_TS?blocking=true -d @request.json


