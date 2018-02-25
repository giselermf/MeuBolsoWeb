from server.dto.base import getResponse, getFilterByCategoryClause, getLimitClause, getSortClause
from server.database.database_connection import run_select, run_update

def get_all_categories():
    return run_select("Select category, subcategory, type, description from Category")

def get_categories(sort, sort_order, filter_param, page_number, per_page):
    sql_comand = "Select * from Category"
    sql_comand += getFilterByCategoryClause(filter_param)
    sql_comand += getSortClause(sort, sort_order)
    sql_comand += getLimitClause(page_number, per_page)

    all_entries = run_select(sql_comand)
    total_records = run_select('select count(*) as total from Category')[0]['total']
    return getResponse('category', total_records, per_page, page_number, all_entries)

def save_category(id, category, description):
    if id == '':
        sql_comand = "insert into Category(Category, Description) values (?, ?)"
        return run_update(sql_comand, (description, category))
    else:
        sql_comand = "update Category set Description = ?, Category = ? where id = ?"
        return run_update(sql_comand, (description, category, int(id)))

def delete_category(id):
    sql_comand = "delete from Category where id = ?"
    return run_update(sql_comand, (id,))