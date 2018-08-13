#!/usr/bin/env python
# author mark_purcell@ie.ibm.com

import json
from db2 import DB2

MAX_INSERT_COUNT = 1000

# insert a double value
SQL_TEMPLATE1 = "CALL {database}('{{device_id}}', TIMESTAMP('{{observed}}'), {{value}})"

# insert a combination double/text value
SQL_TEMPLATE2 = "CALL {database}('{{device_id}}', TIMESTAMP('{{observed}}'), {{value}}, '{{text}}')"

# insert a text value
SQL_TEMPLATE3 = "CALL {database}('{{device_id}}', TIMESTAMP('{{observed}}'), NULL, '{{text}}')"


def gen_statement_insert(database, row):
    '''generate sql insert statment

    returns: (statment, true) on success, (error, false) otherwise
    '''
    sql_template1 = SQL_TEMPLATE1.format(database=database)
    sql_template2 = SQL_TEMPLATE2.format(database=database)
    sql_template3 = SQL_TEMPLATE3.format(database=database)

    sql = ''

    try:
        if 'device_id' not in row:
            return sql

        if 'observed_timestamp' not in row:
            return sql

        did = row['device_id']
        ots = row['observed_timestamp']

        txt, val = None, None
        if 'value' in row:
            val = row['value']
        if 'text' in row:
            txt = row['text']

        if val is not None:
            if type(val) == str:
                # string value - ignore any text
                sql = sql_template3.format(device_id=did, observed=ots, text=val)
            elif txt is not None:
                sql = sql_template2.format(device_id=did, observed=ots, value=val, text=txt)
            else:
                sql = sql_template1.format(device_id=did, observed=ots, value=val)
        elif txt is not None:
            sql = sql_template3.format(device_id=did, observed=ots, text=txt)

    except Exception as err:
        print('error: {}'.format(err))
        return str(err), False

    return sql, True


def process(args):
    '''insert messages into db2'''
    errs = []
    commands = 0
    requested = 0

    try:
        db2 = DB2(args, ['database'])
        count = 0
        sql = ''

        for msg in args['messages']:
            stmt, err = gen_statement_insert(args['database'], msg)
            if not err:
                errs.append(err)
                continue

            sql += stmt + '; '

            count += 1
            if count == MAX_INSERT_COUNT:
                rsp = db2.insert(sql)
                d = rsp.json()
                commands += d['commands_count']
                requested += count
                count = 0
                sql = ''

        if count != 0:
            rsp = db2.insert(sql)
            d = rsp.json()
            commands += d['commands_count']
            requested += count

        retval = {'status': 'success',
                  'requested': requested}
    except Exception as err:
        retval = {'status': 'failed',
                  'requested': requested,
                  'msg': str(err)}
        print('error: {}'.format(err))

    if errs:
        update = {'status': 'warning',
                  'rejected': len(errs),
                  'errors': errs}
        retval.update(update)

    dbg = args.get('debug', False)
    if dbg:
        print(retval)

    return retval


def main(args):
    if 'status' not in args:
        return {'status': 'failure',
                'messages': ['no message status found']}

    if args['status'] != 'success':
        return {'status': 'failure',
                'messages': ['message with status failure found']}

    if 'messages' not in args:
        return {'status': 'failure',
                'messages': ['no messages found']}

    return process(args)
