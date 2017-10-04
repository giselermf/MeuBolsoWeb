import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_name = os.path.join(BASE_DIR, 'dto/dbMeuBolso.db')

def create_connection():
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except Error as e:
        print(e)

def get_categories(sort, sort_order, filter):
    sql_comand = "Select * from Category"
    if filter is not None and filter != "":
        filter = '%' + filter + '%'
        sql_comand += " where Category like '%s' or Description like '%s' " % (filter, filter)
    if sort != '':
        sql_comand += " order by '%s' %s " % (sort, sort_order)
    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute(sql_comand)
        all_entries = c.fetchall()
        array_json = [ {"id": x[0], "Category": x[1], "Description" : x[2] } for x in all_entries  ]
        return json.dumps({"data": array_json})

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

