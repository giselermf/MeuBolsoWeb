from server.dto.base import getResponse, getLimitClause, getSortClause
from server.database.database_connection import run_sql
import json

def get_all_categories():
    return run_sql("Select id, category, subcategory, type, description from vwCategories")

def add_param(column_name, param_value):
    if param_value != None:
        return  "{0} like '%{1}%' and ".format(column_name, param_value)
    return ""

def get_filter_data():
    all_entries = run_sql("Select id, Category, SubCategory, Type from Category")
    return json.dumps(all_entries)

def get_categories(sort, sort_order=None, filter_param=None, page_number=None, per_page=None):
    sql_comand = "Select * from vwCategories"
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

    all_entries = run_sql(sql_comand)
    total_records = run_sql('select count(*) as total from vwCategories ' + where_clause)[0]['total']
    return getResponse('category', total_records, per_page, page_number, all_entries)

def save_category(id, selectedCategoryid, description):
    if id == '':
        sql_comand = "insert into CategoryDescription(description, category_id) values (?, ?)"
        return run_sql(sql_comand, (description, selectedCategoryid))
    else:
        sql_comand = "update CategoryDescription set description = ?, category_id = ? where id = ?"
        return run_sql(sql_comand, (description, selectedCategoryid, int(id)))

def get_category_id(Type, Category, SubCategory):
    sql_command = "SELECT id FROM Category where Type = ? and Category = ? and SubCategory = ?"
    all_results = run_sql(sql_command, (Type, Category, SubCategory))
    if len(all_results)>0:
        return all_results[0]['id']

def delete_category(id):
    sql_comand = "delete from CategoryDescription where id = ?"
    return run_sql(sql_comand, (id,))