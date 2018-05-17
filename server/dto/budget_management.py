from server.database.database_connection import run_select, run_update
from server.dto.base import getResponse
import json
import datetime

def get_budget(filter_param=None):
    sql_command = "Select * from vwBudget "
    where_clause = ""
    if  filter_param != None and filter_param != {} :
        where_clause = " where Date >= '" + filter_param.get("fromDate") + "'"
        where_clause += " and Date <= '" + filter_param.get("toDate") + "'"
    sql_command += where_clause
    sql_command += " order by Year, Month, Type, Category, SubCategory"
    all_entries = run_select(sql_command)
    return getResponse('Budget', None, None, 1, all_entries)

def update_budget(id, CategoryId, Value, Month, Year):
    print('here', id, CategoryId, Value, Month, Year)
    if id == '':
        sql_command = "insert into Budget (category_id, Amount, Month,Year ) VALUES (?,?,?,?)"
        return run_update(sql_command, (CategoryId, Value, Month, Year))
    elif int(Value) == 0:
        sql_command = "delete from Budget where id = ?"
        return run_update(sql_command, (int(id),))
    else:
        sql_command = "update Budget set Amount = ? where id = ?"
        return run_update(sql_command, (Value, int(id)))

def get_cashFlow(filter_param=None):
    today = datetime.datetime.today()
    beginning_of_month = datetime.datetime(today.year, today.month, 1).strftime('%Y-%m-%d')

    if  filter_param != None and filter_param != {} :
        from_date = filter_param.get("fromDate")
        to_date = filter_param.get("toDate")
    else:
        from_date = beginning_of_month
        to_date = datetime.datetime(today.year, 12, 31).strftime('%Y-%m-%d')

    to_date_datetime = datetime.datetime.strptime(to_date, "%Y-%m-%d")

    sql_command = "select 'Real' as Type, date(Year || '-' || substr('0' || Month, -2)  || '-01') as beginMonth, "\
    "Month, Year, sum(AmountEUR) as NetInMonth from "\
    "vwTransactions where Date < '{0}' and Date > '{1}' group by Year, "\
    "Month union select 'Budget' as Type,  date(Year || '-' || substr('0' || Month, -2)  || '-01') as beginMonth, "\
    "Month, Year, sum(Budget) as NetInMonth from vwBudget "\
    "where Month >= {2} and Year >= {3} and Month <= {4} and Year <= {5} group by Month, Year order by beginMonth"\
    .format(beginning_of_month, from_date, today.month, today.year, to_date_datetime.month, to_date_datetime.year)
    all_entries = run_select(sql_command)
    return getResponse('cash_flow', None, None, 1, all_entries)

def get_RunningBalance(filter_param=None):
    if  filter_param != None and filter_param != {} :
        by_date = filter_param.get("byDate")
    else:
        by_date = datetime.datetime.today().strftime('%Y-%m-%d')

    sql_command = "select sum(RunningBalance) as balance from (Select BankName, max(Date), RunningBalance"\
    " from vwTransactions where Date <= '{0}' group by BankName )".format(by_date)

    print(sql_command)
    all_entries = run_select(sql_command)
    return getResponse('RunningBalance', None, None, 1, all_entries)