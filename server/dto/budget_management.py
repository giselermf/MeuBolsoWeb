from server.database.database_connection import run_sql
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
    all_from_budget = run_sql(sql_command)

    all_from_transactions = run_sql("select category_id,  Month, Year, sum(AmountEUR) as Actuals, Type, Category, SubCategory from vwTransactions  " + where_clause + " group by category_id, Month, Year, Type, Category, SubCategory")
    
    all_categories = set(map(lambda x: str(x['category_id'])+"-"+str(x['Month'])+"-"+str(x['Year']), all_from_budget))
    for e in all_from_transactions:
        e_identificator = str(str(e['category_id'])+"-"+str(int(e['Month'])) +"-"+str(e['Year']))
        if e_identificator not in all_from_transactions:
            new_row = {"category_id": e['category_id'], \
            "Month": e['Month'], "Year": e['Year'], "Budget": 0, \
            "Actuals": e['Actuals'], 
            "Type": e['Type'], "Category": e['Category'], "SubCategory": e['SubCategory']}
            all_from_budget.append(new_row)

    return getResponse('Budget', None, None, 1, all_from_budget)

def update_budget(id, CategoryId, Value, Month, Year):
    if id == '':
        sql_command = "insert into Budget (category_id, Amount, Month,Year ) VALUES (?,?,?,?)"
        return run_sql(sql_command, (CategoryId, Value, Month, Year))
    elif int(Value) == 0:
        sql_command = "delete from Budget where id = ?"
        return run_sql(sql_command, (int(id),))
    else:
        sql_command = "update Budget set Amount = ? where id = ?"
        return run_sql(sql_command, (Value, int(id)))

def get_cashFlow(filter_param=None):
    today = datetime.datetime.today()
    beginning_of_current_month = datetime.datetime(today.year, today.month, 1).strftime('%Y-%m-%d')

    if  filter_param != None and filter_param != {} :
        from_date = filter_param.get("fromDate")
        to_date = filter_param.get("toDate")
    else:
        from_date = beginning_of_current_month
        to_date = datetime.datetime(today.year, 12, 31).strftime('%Y-%m-%d')

    to_date_datetime = datetime.datetime.strptime(to_date, "%Y-%m-%d")

    sql_command = "select 'Real' as Type, date(Year || '-' || substr('0' || Month, -2)  || '-01') as beginMonth, "\
    "Month, Year, sum(AmountEUR) as NetInMonth from "\
    "vwTransactions where Date < '{0}' and Date > '{1}' group by Year, "\
    "Month union select 'Budget' as Type,  date(Year || '-' || substr('0' || Month, -2)  || '-01') as beginMonth, "\
    "Month, Year, sum(Budget) as NetInMonth from vwBudget "\
    "where Month >= {2} and Year >= {3} and Month <= {4} and Year <= {5} group by Month, Year order by beginMonth"\
    .format(beginning_of_current_month, from_date, today.month, today.year, to_date_datetime.month, to_date_datetime.year)
    all_entries = run_sql(sql_command)
    return getResponse('cash_flow', None, None, 1, all_entries)

def get_RunningBalance(filter_param=None):
    if  filter_param != None and filter_param != {} :
        by_date = filter_param.get("byDate")
    else:
        by_date = datetime.datetime.today().strftime('%Y-%m-%d')

    sql_command = "select sum(RunningBalance) as balance from (Select BankName, max(Date), RunningBalance"\
    " from vwTransactions where date(Date) <= '{0}' and Active = 1 and AccountType != 'Savings' group by BankName )".format(by_date)

    all_entries = run_sql(sql_command)
    return getResponse('RunningBalance', None, None, 1, all_entries)