#!/usr/bin/env python
#author mark_purcell@ie.ibm.com

import json
import requests
import csv
import datetime
from dateutil.tz import tzutc


class DB2():
    def __init__(self, args, keys):
        keys.extend(['database_rest_url', 'database_userid', 'database_password'])
        for key in keys:
            if args.get(key) is None:
                msg = '{} is missing'.format(key)
                raise Exception(msg)

        self.base_url = args['database_rest_url']

        if not self.base_url.endswith('/'):
            self.base_url += '/'

        self.jobs_url = self.base_url + 'sql_jobs'
        self.auth_url = self.base_url + 'auth'
        self.sql_url = self.base_url + 'sql_query_export'

        self.token = self.fetch_auth_token(args['database_userid'], args['database_password'])
        self.hdr = self.gen_headers(self.token)

    def fetch_auth_token(self, userid, password):
        headers = {}
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'

        data = { 'userid': userid,  'password': password}
        res = requests.post(self.auth_url, json=data, headers=headers)
        return 'Bearer ' + res.json()['token']

    def gen_headers(self, token):
        headers = {}
        headers['Accept'] = 'text/csv'
        headers['Authorization'] = token
        headers['Content-Type'] = 'application/json'
        return headers

    def execute(self, sql):
        msg = { "command": sql } 
        return requests.post(self.sql_url, json=msg, headers=self.hdr)

    def insert(self, sql):
        msg = { "commands": sql,
                "limit": 0,
                "separator": ";",
                "stop_on_error": "no"}
        return requests.post(self.jobs_url, json=msg, headers=self.hdr)

    def fail(self, code, text):
        msResponse = {'status': code, 'state': 'Failed', 'result': text}
        result = msResponse
        return result

    def success(self, msResponse):
        temp = json.dumps(msResponse)
        print("%r" % temp)

        if len(temp) > (1048576/2)-4096:
            self.fail(413, 'Too many results')
        else:
            result = {'status': 200, 'state': 'Success', 'result': msResponse}

        return result

    def string_arg(self, args, field):
        v = args[field]
        if (v is None) or (type(v) != str) or (len(v) == 0):
            raise Exception('Poorly formed \'' + field + '\' field specified.')
        return v

    def date_arg(self, args, field):
        v = self.string_arg(args, field)
        return datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S+00:00')

    def isodate(self, v):
        return datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tzutc()).isoformat()
