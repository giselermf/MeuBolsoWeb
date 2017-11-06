from server.dto.base import create_connection, getResponse, getFilterByCategoryClause, getLimitClause, getSortClause

def get_categories(sort, sort_order, filter_param, page_number, per_page):
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


    