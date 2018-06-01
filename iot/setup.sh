#!/bin/bash
#Author: Mark Purcell

if [[ ! $# -eq 5 ]] ; then
    echo 'Usage: key token org out1 out2'
    exit 1
fi

DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
cd $DIR

pip3 -q install ibmiotf

export WIOT_KEY=$1
export WIOT_TKN=$2
export WIOT_ORG=$3

type1="10101"
device1="800800803"
device2="800800804"

TEMPFILE=./temp_config.json


function add_device_type {
    python3 device.py --action create_type --typeId $type1
    if [ $? -ne 0 ]; then
        return
    fi
}

function add_device {
    python3 device.py --action create --typeId $type1 --deviceId $1 > $TEMPFILE
    if [ $? -ne 0 ]; then
        return
    fi

    sed -i -e '1,1d' $TEMPFILE

    echo -e '{' > $2
    echo -e '\t"org": "'$WIOT_ORG'",' >> $2
    echo -e '\t"type": "'$type1'",' >> $2
    echo -e '\t"id": "'$1'",' >> $2
    echo -e '\t"auth-method": "token",' >> $2
    devtoken=`cat $TEMPFILE | jq '.authToken'`
    echo -e '\t"auth-token": '$devtoken'' >> $2
    echo -e '}' >> $2
    rm $TEMPFILE
}

function list_devices {
    DEVICES=`python3 device.py --action list | jq '.meta.total_rows'`
    echo "Existing devices: " $DEVICES
}

function delete_device {
    python3 device.py --action delete --typeId $type1 --deviceId $1
    if [ $? -ne 0 ]; then
        echo "cant delete device"
        return
    fi
}

function delete_device_type {
    python3 device.py --action delete_type --typeId $type1
    if [ $? -ne 0 ]; then
        echo "cant delete device"
        return
    fi
    python3 device.py --action list_type
}

list_devices

delete_device $device1
delete_device $device2
delete_device_type

add_device_type
add_device $device1 $4
add_device $device2 $5

