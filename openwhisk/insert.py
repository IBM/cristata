#!/usr/bin/env python
#author mark_purcell@ie.ibm.com

import json
import os 
import requests
from db2 import DB2

MAX_INSERT_COUNT = 1000

#Insert a double value
SQL_TEMPLATE1 = 'CALL {database}(\'{{device_id}}\', TIMESTAMP(\'{{observed}}\'), {{value}});'

#Insert a text value
SQL_TEMPLATE2 = 'CALL {database}(\'{{device_id}}\', TIMESTAMP(\'{{observed}}\'), NULL, \'{{value}}\');'


def gen_insert(database, m):
    sql_template1 = SQL_TEMPLATE1.format(database=database)
    sql_template2 = SQL_TEMPLATE2.format(database=database)

    if type(m) == str:
        args = json.loads(m)
    else:
        args = m

    sql = ''

    try:
        t = args['insert_args']['device_id']
        o = args['insert_args']['observed_timestamp']
        v = args['insert_args']['value']

        if type(v) == str:
            sql += sql_template2.format(device_id=t, observed=o, value=v)
        else:
            sql += sql_template1.format(device_id=t, observed=o, value=v)
    except Exception as e:
        print('Error: %r' % e)
        return str(e), False

    return sql, True


def main(args):
    if 'messages' not in args:
        return {'status': 'failure', 'msg': ['no messages found']}

    err = []
    commands = 0
    requested = 0

    try:
        db2 = DB2(args, ['database'])
        count = 0
        sql = ''

        for m in args['messages']:
            s, r = gen_insert(args['database'], m['value'])
            if not r:
                err.append(s)
                continue

            sql += s + '; '

            count += 1
            if count == MAX_INSERT_COUNT:
                r = db2.insert(sql)
                d = r.json()
                commands += d['commands_count']
                requested += count
                count = 0
                sql = ''

        if count != 0:
            r = db2.insert(sql)
            d = r.json()
            commands += d['commands_count']
            requested += count

        retval = {'status': 'ok', 'requested' : requested }
    except Exception as e:
        retval = {'status': 'failed', 'requested' : requested, 'msg': str(e)}
        print("Error : %r" % e)

    if len(err) > 0:
        retval.update({'status': 'warning', 'rejected': len(err), 'errors': err})

    dbg = args.get('debug', False)
    if dbg:
        print(retval)

    return retval


