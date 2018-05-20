from server.dto.base import getResponse, getLimitClause, getSortClause
from server.database.database_connection import run_select, run_update, create_connection
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
        where_clause += add_param('Category', "=", filter_param.get('Category') )
        where_clause += add_param('SubCategory', "=", filter_param.get('SubCategory') )
        where_clause += add_param('Type', "=", filter_param.get('Type') )
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
    total_records = run_select('select count(*) as total from vwTransactions ' + where_clause )[0]['total']
    return getResponse('transactions', total_records, per_page, page_number, all_entries)

def get_transaction(currency, bank_name, amount, date_str, description, transaction_number=None):
    sql_command = "SELECt * FROM vwTransactions where Currency='{0}' and bankname='{1}' and Amount={2} and Date_str='{3}'"\
                    " and Description like '{4}%' "\
                    .format(currency, bank_name, amount, date_str, description)
    if transaction_number is not None:
        sql_command = sql_command + " and TransactionNumber = '{0}'  ".format(transaction_number)
    return run_select(sql_command)

def insert_transaction(category_id, description, transaction_number, currency, amount, bank_name, amount_eur, date_str, date ):
    sql_commnad = 'INSERT INTO Transactions '\
    '(category_id,Description,TransactionNumber,Currency,Amount,Date_str,BankName,AmountEUR,Date,Year, Month, Day)'\
    'VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
    return run_update(sql_commnad, (category_id, description, transaction_number, currency, amount, date_str, bank_name, amount_eur, date, date.year, date.month, date.day)  )

def update_transaction(transaction_id, category_id=None, transaction_number= None, RunningBalance=None):
    if transaction_id == '' or transaction_id==None:
        return json.dumps({"data": 'fail'})
    else:
        sql_command = "update Transactions set "
        if category_id is not None:
            sql_command += " category_id = {0} ,".format(category_id)
        if transaction_number is not None:
            sql_command += " TransactionNumber = {0} ,".format(transaction_number)
        if RunningBalance is not None:
            sql_command += " RunningBalance = {0} ,".format(RunningBalance)
        sql_command = sql_command[:-1] + " where id = ? "
        return run_update(sql_command, (transaction_id,))

def split_transaction(transactionId, newAmountEUR, newCategoryId):
    sql_command1 =  "update Transactions set AmountEUR = AmountEUR - ? where id = ?;"
    sql_command2 = "INSERT INTO Transactions ( Description,TransactionNumber, Currency, Amount, Date_str, "\
        "BankName, AmountEUR, RunningBalance, Date, Year, Month, Day, category_id )"\
        "SELECT Description, TransactionNumber, Currency, 0, Date_str, BankName, ?, RunningBalance, Date, Year, Month, Day, ?  FROM Transactions where id = ?;"
    conn = create_connection()
    with conn:
        c = conn.cursor()
        try:
            c.execute(sql_command1, (int(newAmountEUR), int(transactionId)))
            c.execute(sql_command2, (int(newAmountEUR), int(newCategoryId), int(transactionId)))
            conn.commit()
            return json.dumps({"data": 'sucess'})
        except:
            print('on except', sql_command1, sql_command2)
            raise
