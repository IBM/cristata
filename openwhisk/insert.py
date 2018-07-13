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
SQL_TEMPLATE2 = 'CALL {database}(\'{{device_id}}\', TIMESTAMP(\'{{observed}}\'), NULL, \'{{text}}\');'

#Insert a combination double/text value
SQL_TEMPLATE3 = 'CALL {database}(\'{{device_id}}\', TIMESTAMP(\'{{observed}}\'), {{value}}, \'{{text}}\');'


def gen_insert(database, m):
    sql_template1 = SQL_TEMPLATE1.format(database=database)
    sql_template2 = SQL_TEMPLATE2.format(database=database)
    sql_template3 = SQL_TEMPLATE3.format(database=database)

    if type(m) == str:
        args = json.loads(m)
    else:
        args = m

    sql = ''

    try:
        for row in args:
            if 'device_id' not in row:
                continue
            if 'observed_timestamp' not in row:
                continue

            i = row['device_id']
            o = row['observed_timestamp']

            t, v = None, None
            if 'value' in row:
                v = row['value']
            if 'text' in row:
                t = row['text']

            if v is not None:
                if type(v) == str:
                    #string value - ignore any text
                    sql += sql_template2.format(device_id=i, observed=o, text=v)
                elif t is not None:
                    sql += sql_template3.format(device_id=i, observed=o, value=v, text=t)
                else:
                    sql += sql_template1.format(device_id=i, observed=o, value=v)
            elif t is not None:
                sql += sql_template2.format(device_id=i, observed=o, text=t)
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


