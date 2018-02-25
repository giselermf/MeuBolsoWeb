import json
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_name = os.path.join(BASE_DIR, 'database/dbMeuBolso.db')

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
    except:
        print('error')
        raise 

def run_select(sql_command, param_name=None):
    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute(sql_command)
        if param_name is None:
            return c.fetchall()
        else:
            return json.dumps({param_name: c.fetchall()})

def run_update(sql_command, *params):
    conn = create_connection()
    with conn:
        c = conn.cursor()
        print(sql_command)
        c.execute(sql_command, *params)
        conn.commit()
        return json.dumps({"data": 'sucess'})