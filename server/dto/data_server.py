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

def getSortClause(sort, sort_order):
    if sort is not None and sort != '':
        return " order by '%s' %s " % (sort, sort_order)
    return ''

def getFilterClause(filter_param):
    if filter_param is not None and filter_param != "":
        filter_param = '%' + filter_param + '%'
        return " where Category like '%s' or Description like '%s' " % (filter_param, filter_param)
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
    total_records = int(total_records)
    per_page = int(per_page)
    page_number = int(page_number)
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

def get_transactions(sort, sort_order, filter_param, page_number, per_page):
    sql_comand = "Select * from Transactions"
    sql_comand += getFilterClause(filter_param)
    sql_comand += getSortClause(sort, sort_order)
    sql_comand += getLimitClause(page_number, per_page)
    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute('select count(*) as total from Transactions')
        total_records = int(c.fetchone()['total'])
        c.execute(sql_comand)
        all_entries = c.fetchall()
        return getResponse('transactions', total_records, per_page, page_number, all_entries)

def get_categories(sort, sort_order, filter_param, page_number, per_page):
    conn = create_connection()
    sql_comand = "Select * from Category"
    sql_comand += getFilterClause(filter_param)
    sql_comand += getSortClause(sort, sort_order)
    sql_comand += getLimitClause(page_number, per_page)

    with conn:
        c = conn.cursor()
        c.execute('select count(*) as total from Category')
        total_records = int(c.fetchone()['total'])
        c.execute(sql_comand)
        all_entries = c.fetchall()
        return getResponse('category', total_records, per_page, page_number, all_entries)

def save_transaction(id, category, sub_category):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    conn = create_connection()
    with conn:
        c = conn.cursor()
        if id == '':
            return json.dumps({"data": 'fail'})
        else:
            sql_comand = "update Transactions set SubCategory = ?, Category = ? where id = ?"
            c.execute(sql_comand, (sub_category, category, int(id)))
        conn.commit()
        return json.dumps({"data": 'sucess'})

def save_category(id, category, description):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    conn = create_connection()
    with conn:
        c = conn.cursor()
        if id == '':
            sql_comand = "insert into Category(Category, Description) values (?, ?)"
            c.execute(sql_comand, (description, category))
        else:
            sql_comand = "update Category set Description = ?, Category = ? where id = ?"
            c.execute(sql_comand, (description, category, int(id)))
        conn.commit()
        return json.dumps({"data": 'sucess'})

def delete_category(id):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    sql_comand = "delete from Category where id = ?"
    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute(sql_comand, (id,))
        conn.commit()
        return json.dumps({"data": 'sucess'})

