import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_name = os.path.join(BASE_DIR, 'dto/dbMeuBolso.db')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_connection():
    try:
        conn = sqlite3.connect(database_name)
        conn.row_factory = dict_factory
        return conn
    except Error as e:
        print(e)

def getFilterClause(filter_param):
    if filter_param is not None and filter_param != "":
        filter_param = '%' + filter_param + '%'
        return " where Category like '%s' or Description like '%s' " % (filter_param, filter_param)
    return ''

def getSortClause(sort, sort_order):
    if sort is not None and sort != '':
        return " order by '%s' %s " % (sort, sort_order)
    return ''

def getLimitClause( page_number, per_page):
    if page_number is not None and per_page is not None:
        try:
            page_number = int(page_number)
            per_page = int(per_page)    
            clause = " limit %d, %d " % ((per_page * (page_number-1)), per_page)
            return clause
        except e:
            print('error', e)
            return ''
    return ''

def getResponse(url, total_records, per_page, page_number, all_entries): 
    total_records = 0 if total_records is None else int(total_records)
    per_page = 1 if per_page is None else int(per_page)
    page_number = 0 if page_number is None else int(page_number)
    response = {}
    response['per_page'] = per_page
    response['current_page'] = page_number
    response['last_page'] = int(total_records/per_page)
    response['total'] = total_records
    response['next_page_url'] = "%s?page=%s" % (url, page_number+1)
    response['prev_page_url'] = "%s?page=%s" % (url, page_number-1)
    response['from'] = int ((page_number -1) * per_page + 1) 
    response['to'] = response['from'] + per_page
    response['data'] = all_entries
    return json.dumps(response)