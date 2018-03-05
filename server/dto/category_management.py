from server.dto.base import getResponse, getLimitClause, getSortClause
from server.database.database_connection import run_select, run_update

def get_all_categories():
    return run_select("Select category, subcategory, type, description from Category")

def add_param(column_name, param_value):
    if param_value != None:
        return  "{0} like '%{1}%' and ".format(column_name, param_value)
    return ""

def get_categories(sort, sort_order=None, filter_param=None, page_number=None, per_page=None):
    sql_comand = "Select * from Category"
    where_clause  = ""
    if  filter_param != None and filter_param != {} :
        where_clause = " where "
        where_clause += add_param('type', filter_param.get('type') )
        where_clause += add_param('category', filter_param.get('category') )
        where_clause += add_param('subcategory', filter_param.get('subcategory') )
        where_clause += add_param('description', filter_param.get('description') )
        k = where_clause.rfind("and")
        where_clause = where_clause[:k]
    sql_comand += where_clause
    sql_comand += getSortClause(sort, sort_order)
    sql_comand += getLimitClause(page_number, per_page)

    all_entries = run_select(sql_comand)
    print(sql_comand)
    total_records = run_select('select count(*) as total from Category ' + where_clause)[0]['total']
    return getResponse('category', total_records, per_page, page_number, all_entries)

def save_category(id, type, category, subcategory, description):
    if id == '':
        sql_comand = "insert into Category(type, category, subcategory, description) values (?, ?, ?, ?)"
        return run_update(sql_comand, (type, category, subcategory, description))
    else:
        sql_comand = "update Category set Description = ?, type = ?, Category = ? , subcategory = ? where id = ?"
        return run_update(sql_comand, (description, type, category, subcategory, int(id)))

def delete_category(id):
    sql_comand = "delete from Category where id = ?"
    return run_update(sql_comand, (id,))