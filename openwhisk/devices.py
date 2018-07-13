#!/usr/bin/env python
#author mark_purcell@ie.ibm.com

import json
import os 
import requests
import csv
from db2 import DB2

SQL_TEMPLATE = ''
SQL_TEMPLATE += 'CALL {database}(); '


def build_query(database):
    sql_template = SQL_TEMPLATE.format(database=database)
    return sql_template, True

def process_response(text):
    t = []
    rows = text.split('\n')

    if len(rows) > 0:
        reader = csv.reader(rows, delimiter=',', lineterminator='\\n')

        for row in reader:
            if len(row) > 0:
                t.append(row[0])

    return { 'devices': t, 'deviceCount': len(t), 'deviceMetadata': ["Device Id"] }


def main(args):
    print('Args %r' % args)

    result = {}

    try:
        db2 = DB2(args, ['database', 'database_userid', 'database_password', 'database_rest_url'])

        sql, r = build_query(args['database'])
        r = db2.execute(sql)

        if r.status_code != 200:
            raise Exception(r.json())    

        response = process_response(r.text)
        result = db2.success(response)
    except Exception as e:
        result = {'status': 400, 'state': 'Failed', 'result': str(e)}
        print('Error: %r' % result)

    dbg = args.get('debug', False)
    if dbg:
        print('%r' % result)
		
    return result

