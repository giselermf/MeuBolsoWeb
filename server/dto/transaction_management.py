from server.dto.base import getResponse, getLimitClause, getSortClause
from server.database.database_connection import run_select, run_update
import json

def get_all_transactions(oder_by=None):
    sql_command = "Select id, category, subcategory, type, description, BankName, AmountEUR,Amount, Date, Year, Month from vwTransactions"
    if oder_by is not None:
        sql_command += " order by " + oder_by
    return run_select(sql_command)


def add_param(column_name, comparison, param_value):
    if param_value != None:
        if comparison == 'in':
            return "{0} {1} ('{2}') and ".format(column_name, comparison, "','".join(param_value))
        if comparison == 'like':
            return "{0} {1} '%{2}%' and ".format(column_name, comparison, param_value)
        else:
            return "{0} {1} '{2}' and ".format(column_name, comparison, param_value)
    return ""

def get_filter_transaction_data(): 
    all_entries = run_select("Select distinct BankName, category, subCategory, type from vwTransactions where Active=1")
    return json.dumps(all_entries)
    
def get_transactions_filtered(sort, sort_order, filter_param, page_number, per_page):
    sql_command = "select * from vwTransactions "
    where_clause = ""
    if  filter_param != None and filter_param != {} :
        where_clause = " where "
        where_clause += add_param('bankName', '=', filter_param.get('bankName') )
        where_clause += add_param('Category', "in", filter_param.get('Categories') )
        where_clause += add_param('SubCategory', "in", filter_param.get('SubCategories') )
        where_clause += add_param('Type', "in", filter_param.get('Types') )
        where_clause += add_param('Description', "like", filter_param.get('Description') )
        where_clause += add_param('SubCategory', "like", filter_param.get('SubCategory') )
        where_clause += add_param('AmountEUR', '>=',filter_param.get('fromAmount') )
        where_clause += add_param('AmountEUR', '<=',filter_param.get('toAmount') )
        where_clause += add_param('Date', '>=',filter_param.get('fromDate') )
        where_clause += add_param('Date', '<=',filter_param.get('toDate') )
        where_clause += add_param('Currency', 'in',filter_param.get('Currencies') )
        k = where_clause.rfind("and")
        where_clause = where_clause[:k]
    sql_command += where_clause
    sql_command += getSortClause(sort, sort_order)
    sql_command += getLimitClause(page_number, per_page)
    all_entries = run_select(sql_command)
    print('***', sql_command)
    total_records = run_select('select count(*) as total from vwTransactions ' + where_clause )[0]['total']
    return getResponse('transactions', total_records, per_page, page_number, all_entries)

def get_transaction(currency, bank_name, amount, date_str, description, transaction_number=None):
    sql_command = "SELECt * FROM vwTransactions where Currency='{0}' and bankname='{1}' and Amount={2} and Date_str='{3}'"\
                    " and Description like '{4}%' "\
                    .format(currency, bank_name, amount, date_str, description)
    if transaction_number is not None:
        sql_command = sql_command + " and TransactionNumber = '{0}'  ".format(transaction_number)
    return run_select(sql_command)

def insert_transaction(category, sub_category, entry_type, description, transaction_number, currency, amount, bank_name, amount_eur, date_str, date ):
    sql_commnad = 'INSERT INTO Transactions '\
    '(Category,SubCategory,Type,Description,TransactionNumber,Currency,Amount,Date_str,BankName,AmountEUR,Date,Year, Month, Day)'\
    'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    return run_update(sql_commnad, (category, sub_category, entry_type, description, transaction_number, currency, amount, date_str, bank_name, amount_eur, date, date.year, date.month, date.day)  )
    #print('new entry', category, sub_category, entry_type, description, transaction_number, currency, amount, bank_name, amount_eur, date)
    #return json.dumps({"data": 'sucess'})

def update_transaction(id, category=None, sub_category=None, type=None, transaction_number= None, RunningBalance=None):
    if id == '' or id==None:
        return json.dumps({"data": 'fail'})
    else:
        sql_command = "update Transactions set "
        if category is not None:
            sql_command += " ategory = '{0}' ,".format(category)
        if sub_category is not None:
            sql_command += " subcategory = '{0}' ,".format(sub_category)
        if type is not None:
            sql_command += " type = '{0}' ,".format(type)
        if transaction_number is not None:
            sql_command += " TransactionNumber = {0} ,".format(transaction_number)
        if RunningBalance is not None:
            sql_command += " RunningBalance = {0} ,".format(RunningBalance)
        sql_command = sql_command[:-1] + " where id = ? "
        return run_update(sql_command, (id,))
