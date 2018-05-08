from server.database.database_connection import run_select, run_update
from server.dto.base import getResponse
import json

def get_budget(filter_param=None):
    print('HERE',  filter_param)
    sql_command = "Select * from vwBudget "
    where_clause = ""
    if  filter_param != None and filter_param != {} :
        where_clause = " where BudgetDate >= '" + filter_param.get("fromDate") + "'"
        where_clause += " and BudgetDate <= '" + filter_param.get("toDate") + "'"
    sql_command += where_clause
    sql_command += " order by Year, Month"
    all_entries = run_select(sql_command)
    return getResponse('Budget', None, None, 1, all_entries)

def update_budget(id, CategoryId, Value, Month, Year):
    if id == '':
        sql_comand = "insert into Budget (category_id, Amount, Month,Year ) VALUES (?,?,?,?)"
        return run_update(sql_comand, (CategoryId, Value, Month, Year))
    else:
        sql_comand = "update Budget set Amount = ? where id = ?"
        return run_update(sql_comand, (Value, int(id)))
