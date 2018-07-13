'''publish single message to Watson IoT'''
import json
import time
import sys

import ibmiotf.device


def published():
    '''publish callback'''
    print('--published--\n')


def publish(config_file):
    '''parse config file and publish message'''

    try:
        with open(config_file) as cfile:
            config = json.load(cfile)

        client = ibmiotf.device.Client(config)
        client.connect()
        qos = 2  # Quality of service: exactly once

        my_data = [
		{ "observed_timestamp": "2018-04-22 13:24:23", "device_id": "1", "value": 52.2 },
		{ "observed_timestamp": "2018-04-22 13:24:24", "device_id": "1", "value": 57.2 },
		{ "observed_timestamp": "2018-04-22 13:24:25", "device_id": "1", "value": "something" },
		{ "observed_timestamp": "2018-04-22 13:24:26", "device_id": "1", "text": "something else" },
		{ "observed_timestamp": "2018-04-22 13:24:27", "device_id": "1", "value": 444.22, "text": "more" }
	]
        success = client.publishEvent('status', 'json', my_data, qos, on_publish=published)
        if not success:
            print('failed to publish message')

        time.sleep(5)
        client.disconnect()

    except BaseException as err:
        print('publish failed: %r' % err)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        publish(sys.argv[1])
    else:
        print('usage: {} <config file>'.format(sys.argv[0]))
