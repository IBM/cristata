#!/usr/bin/env python
#author mark_purcell@ie.ibm.com

import json
import requests
import csv
import os 
from db2 import DB2

SQL_TEMPLATE = ''
SQL_TEMPLATE += 'CALL {database}('
SQL_TEMPLATE += '\'{device}\', TIMESTAMP(\'{from_time}\'), TIMESTAMP(\'{to_time}\')'
SQL_TEMPLATE += '); '


def build_query(db2, database, m):
    if type(m) == str:
        args = json.loads(m)
    else:
        args = m

    device = db2.string_arg(args, 'device_id')
    from_time = db2.date_arg(args, 'from')
    to_time = db2.date_arg(args, 'to')
    sql = SQL_TEMPLATE.format(database=database, device=device, from_time=from_time, to_time=to_time)
    return sql, True

def process_response(db2, text):
    t = []

    rows = text.split('\n')

    if len(rows) > 0:
        reader = csv.reader(rows, delimiter=',', lineterminator='\\n')

        for row in reader:
            if len(row) > 1:
                d = db2.isodate(row[1])
                num_v = None

                try:
                    num_v = float(row[2])
                except:
                    pass

                v = [ d, num_v, row[3] ]
                t.append(v)

    return { 'timeseries': t, 'timeseriesRows': len(t), 'timeseriesMetadata': ["observedTimestampUTC","value","text"] }


def main(args):
    #Expecting e.g.
    #{'args': {'from': '2009-07-13T00:00:00+0000', 'device_id': xxxx, 'to': '2017-07-14T01:00:00+0000'}}
    print('Args %r' % args)

    result = {}

    try:
        db2 = DB2(args, ['database', 'database_userid', 'database_password', 'database_rest_url'])

        sql, r = build_query(db2, args['database'], args['args'])
        r = db2.execute(sql)

        if r.status_code != 200:
            raise Exception(r.json())

        response = process_response(db2, r.text)
        result = db2.success(response)
    except Exception as e:
        result = db2.fail(400, str(e))
        print('Error: %r' % str(e))

    return result
