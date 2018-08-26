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
        print('error creating connection')
        raise 

def run_sql(sql_command, *params):
    conn = create_connection()
    with conn:
        c = conn.cursor()
        try:
            print("***", sql_command, *params)
            c.execute(sql_command, *params)
            conn.commit()
            if 'select' in sql_command.lower():
                return c.fetchall()
            else: 
                return json.dumps({"data": 'sucess'})
        except:
            print('on except', sql_command, 'params', *params)
            raise