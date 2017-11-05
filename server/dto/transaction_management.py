from server.dto.base import create_connection, getResponse, getFilterByCategoryClause, getLimitClause, getSortClause

def get_transactions(sort, sort_order, filter_param, page_number, per_page):
    sql_comand = "Select * from Transactions"
    sql_comand += getFilterByCategoryClause(filter_param)
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

    conn = create_connection()
    sql_comand = "Select * from Category"
    sql_comand += getFilterByCategoryClause(filter_param)
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

