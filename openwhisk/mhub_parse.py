#!/usr/bin/env python
#author mark_purcell@ie.ibm.com

'''parse message fromm message hub'''
import json


def process(args):
    ''' process data coming from Message Hub
    
        data fromm Message Hub looks like,
        {
          'messages':
          [
            {
              'partition': 0,
              'key': '{\"orgId\":\"abcdef\",\"deviceType\":\"10101\",\"deviceId\":\"800800803\",\"eventType\":\"status\",\"format\":\"json\",\"timestamp\":\"2018-08-13T08:54:18.966Z\"}',
              'offset': 2,
              'topic': 'watson-iot',
              'value': '[{\"observed_timestamp\": \"2018-04-22 13:24:23\", \"value\": 52.2, \"device_id\": \"1\"}, {\"observed_timestamp\": \"2018-04-22 13:24:24\", \"value\": 57.2, \"device_id\": \"1\"}, {\"observed_timestamp\": \"2018-04-22 13:24:25\", \"value\": \"something\", \"device_id\": \"1\"}, {\"observed_timestamp\": \"2018-04-22 13:24:26\", \"text\": \"something else\", \"device_id\": \"1\"}, {\"observed_timestamp\": \"2018-04-22 13:24:27\", \"text\": \"more\", \"value\": 444.22, \"device_id\": \"1\"}]'
            },
            ...
          ]
        }
        returns,

        {
          'status': 'success',
          'messages':
          [
            {
              'observed_timestamp': '2018-04-22 13:24:23',
              'value': 52.2,
              'device_id': '1'
            },
            {
              'observed_timestamp': '2018-04-22 13:24:24',
              'value': 57.2,
              'device_id': '1'
            },
            {
              'observed_timestamp': '2018-04-22 13:24:25',
              'value': 'something',
              'device_id': '1'
            },
            {
              'observed_timestamp': '2018-04-22 13:24:26',
              'text': 'something else',
              'device_id': '1'
            },
            {
              'observed_timestamp': '2018-04-22 13:24:27',
              'text': 'more',
              'value': 444.22,
              'device_id': '1'
            }
          ]
        }
    '''

    try:
        if 'messages' not in args:
            return {'status': 'failure', 'messages': ['no messages found']}

        values = []
        for message in args['messages']:
            if 'value' in message:
                value = json.loads(message['value'])
                # this produces an array of json objects
                for v in value:
                    values.append(v)

        if len(values) == 0:
            return {'status': 'failure', 'messages': ['no values found']}

        return {'status': 'success', 'messages': values}
    except Execption as e:
        print('error: {}'.format(e))
        return {'status': 'failure', 'messages': ['exception thrown']}


def main(args):
    return process(args)
