#!/usr/bin/env python
#author mark_purcell@ie.ibm.com

import json
import os 
import requests
from db2 import DB2

MAX_INSERT_COUNT = 1000

SQL_TEMPLATE = ''
SQL_TEMPLATE += 'CALL {database}('
SQL_TEMPLATE += '\'{{device_id}}\', TIMESTAMP(\'{{observed_timestamp}}\'), {{value}}'
SQL_TEMPLATE += ')'


def gen_insert(database, m):
    sql_template = SQL_TEMPLATE.format(database=database)

    if type(m) == str:
        args = json.loads(m)
    else:
        args = m

    try:
        t = args['insert_args']['device_id']
        o = args['insert_args']['observed_timestamp']
        v = args['insert_args']['value']

        if type(v) == str:
            v = float(v)

        #value could arrive as NaN
        if (v is None) or (v != v):
            err = {'device_id': t, 'observed_timestamp': o, 'value': v }
            return err, False
    except Exception as e:
        print('Error: %r' % e)
        return str(e), False

    sql = sql_template.format(device_id = t, observed_timestamp = o, value = v)
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


