import ibmiotf
import ibmiotf.application
import logging
import json

import wiot_env

import argparse

parser = argparse.ArgumentParser(description='Sample Messenger client')
parser.add_argument('--deviceId', action='store', dest='deviceId', help='device id')
parser.add_argument('--typeId', action='store', dest='typeId', help='device type id')
parser.add_argument('--authToken', action='store', dest='authToken', help='token', default=None)
parser.add_argument('--action', action='store', dest='action',
                        required=True, 
                        choices=['create', 'delete', 'list', 'create_type', 'delete_type', 'list_type'],
                        help='action create/delete/list/create_type/delete_type/list_type'
)
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

apiOptions = {
    "org": wiot_env.WIOT_ORG,
    "id": "unique_application_name",
    "auth-method": "apikey",
    "auth-key": wiot_env.WIOT_KEY,
    "auth-token": wiot_env.WIOT_TKN
}

metadata2 = {
    "customField1": "customValue3",
    "customField2": "customValue4"
}

deviceInfo = {
    "serialNumber": "101",
    "manufacturer": "virtual",
    "model": "101",
    "deviceClass": "A",
    "descriptiveLocation" : "virtual",
    "fwVersion" : "1.0.1",
    "hwVersion" : "12.01"
}

location = {
    "longitude" : "122.78",
    "latitude" : "37.90",
    "elevation" : "40",
    "accuracy" : "100",
    "measuredDateTime" : "1984-05-12T02:45:11.662Z"
}

apiCli = ibmiotf.api.ApiClient(apiOptions, logger)

if args.action == 'create':
    print("Registering a new device...")   
    response = apiCli.registerDevice(args.typeId, args.deviceId, None, 
						deviceInfo, location, metadata2)
    print(json.dumps((response)))
elif args.action == 'delete':
    try:
        response = apiCli.deleteDevice(args.typeId, args.deviceId)
        print("delete device : " + json.dumps(response))
    except:
        pass
elif args.action == 'list':
    response = apiCli.getDevices({'typeId': args.typeId})
    print(json.dumps((response)))
elif args.action == 'delete_type':
    try:
        print("Deleting device type...")   
        response = apiCli.deleteDeviceType(args.typeId)
    except:
        pass
elif args.action == 'create_type':
    print("Registering a new device type...")   
    deviceInfo = [deviceInfo]
    metadata1 = {"customField11": "customValue11", "customField12": "customValue12"}
    metadata2 = {"customField21": "customValue21", "customField22": "customValue22"}
    metadata = [metadata1]

    for d, m in zip(deviceInfo, metadata):
        response = apiCli.addDeviceType(args.typeId, deviceInfo=d, metadata=m)
        print("registered device type: " + json.dumps(response))
elif args.action == 'list_type':
    response = apiCli.getDeviceTypes()
    print("device types: " + json.dumps(response))


