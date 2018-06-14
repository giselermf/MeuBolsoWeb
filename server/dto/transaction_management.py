from server.dto.base import getResponse, getLimitClause, getSortClause
from server.database.database_connection import run_sql, create_connection
import json

def get_all_transactions(MinDate, BankName=None, oder_by=None):
    sql_command = "Select id, Category, SubCategory, Type, Description, BankName, AmountEUR,Amount, Date, Year, Month from vwTransactions where Date >= ? "
    params = (MinDate,)
    if BankName is not None:
        params = params + (BankName,)
        sql_command += " and BankName = ? "
    if oder_by is not None:
        sql_command += oder_by
    print(sql_command, params)
    return run_sql(sql_command, params)


def add_param(column_name, comparison, param_value):
    if param_value != None:
        if comparison == 'in':
            return "{0} {1} ('{2}') and ".format(column_name, comparison, "','".join(param_value))
        if comparison == 'like':
            return "{0} {1} '%{2}%' and ".format(column_name, comparison, param_value)
        elif type(param_value) is str:
            return "{0} {1} '{2}' and ".format(column_name, comparison, param_value)
        else:
            return "{0} {1} {2} and ".format(column_name, comparison, param_value)
    return ""

def get_filter_transaction_data(): 
    all_entries = run_sql("Select distinct BankName, category, subCategory, type from vwTransactions where Active=1")
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
        if filter_param.get('fromAmount') is not None:
            where_clause += add_param('AmountEUR', '>=', float(filter_param.get('fromAmount')))
        if filter_param.get('toAmount') is not None:
            where_clause += add_param('AmountEUR', '<=', float(filter_param.get('toAmount') ))
        where_clause += add_param('Date', '>=',filter_param.get('fromDate') )
        where_clause += add_param('Date', '<=',filter_param.get('toDate') )
        where_clause += add_param('Currency', 'in',filter_param.get('Currencies') )
        k = where_clause.rfind("and")
        where_clause = where_clause[:k]
    sql_command += where_clause
    sql_command += getSortClause(sort, sort_order)
    sql_command += getLimitClause(page_number, per_page)
    print(sql_command)
    all_entries = run_sql(sql_command)
    total_records = run_sql('select count(*) as total from vwTransactions ' + where_clause )[0]['total']
    return getResponse('transactions', total_records, per_page, page_number, all_entries)

def get_transaction(currency, bank_name, amount, date, description, transaction_number=None):
    sql_command = "SELECt * FROM vwTransactions where Currency='{0}' and bankname='{1}' and Amount={2} and Date='{3}'"\
                    " and Description like '{4}%' "\
                    .format(currency, bank_name, amount, date, description)
    if transaction_number is not None:
        sql_command = sql_command + " and TransactionNumber = '{0}'  ".format(transaction_number)
    return run_sql(sql_command)

def insert_transaction(Description, TransactionNumber, Currency, Amount, BankName, AmountEUR, Date, category_id, RunningBalance=None):
    sql_commnad = 'INSERT INTO Transactions '\
    '(category_id,Description,TransactionNumber,Currency,Amount,BankName,AmountEUR,Date, RunningBalance)'\
    'VALUES (?,?,?,?,?,?,?,?,?)'
    return run_sql(sql_commnad, (category_id, Description, TransactionNumber, Currency, Amount, BankName, AmountEUR, Date, RunningBalance)  )

def update_transaction(transaction_id=None, Description=None ,TransactionNumber=None ,Currency=None ,\
Amount=None , BankName =None,AmountEUR =None, Date =None, category_id=None, RunningBalance=None):
    if transaction_id == '' or transaction_id==None:
        return insert_transaction(Description, TransactionNumber, Currency, Amount, BankName, AmountEUR, Date, category_id, RunningBalance)
    else:
        sql_command = "update Transactions set "
        if category_id is not None:
            sql_command += " category_id = {0} ,".format(category_id)
        if TransactionNumber is not None:
            sql_command += " TransactionNumber = {0} ,".format(TransactionNumber)
        if RunningBalance is not None:
            sql_command += " RunningBalance = {0} ,".format(RunningBalance)
        sql_command = sql_command[:-1] + " where id = ? "
        print('update', sql_command, transaction_id)
        return run_sql(sql_command, (transaction_id,))

def split_transaction(transactionId, newAmountEUR, newCategoryId):
    sql_command1 =  "update Transactions set AmountEUR = ? where id = ?;"
    sql_command2 = "INSERT INTO Transactions ( Description,TransactionNumber, Currency, Amount, "\
        "BankName, AmountEUR, RunningBalance, Date, category_id )"\
        "SELECT Description, TransactionNumber, Currency, 0, BankName, ?, RunningBalance, Date, ?  FROM Transactions where id = ?;"
    conn = create_connection()
    with conn:
        c = conn.cursor()
        try:
            c.execute(sql_command1, (float(newAmountEUR), int(transactionId)))
            c.execute(sql_command2, (float(newAmountEUR), int(newCategoryId), int(transactionId)))
            conn.commit()
            return json.dumps({"data": 'sucess'})
        except:
            print('on except', sql_command1, sql_command2)
            raise

def save_transfer(transaction_id ,TransactionNumber ,Currency ,Amount , toSelectedBank ,AmountEUR , Date , category_id, oldTransferId):
    sql_update_source = "update Transactions set TransferTo = ?, TransferId = ? where id = ?;"
    delete_old_transfer = "delete from Transactions where id = ?"
    sql_insert_new_transaction = 'INSERT INTO Transactions '\
    '(category_id,Description,TransactionNumber,Currency,Amount,BankName,AmountEUR,Date)'\
    'VALUES (?,?,?,?,?,?,?,?)'
    conn = create_connection()
    with conn:
        c = conn.cursor()
        try:
            if (oldTransferId != ''):
                c.execute(delete_old_transfer, (int(oldTransferId),))
            c.execute(sql_insert_new_transaction, (int(category_id), 'Transfer', transaction_id, Currency, -float(Amount), toSelectedBank, -float(AmountEUR), Date))
            c.execute(sql_update_source, (toSelectedBank, c.lastrowid, int(transaction_id)))
            conn.commit()
            update_running_balance(BankName=toSelectedBank)
            return json.dumps({"data": 'sucess'})
        except:
            print('on except', sql_update_source, sql_insert_new_transaction)
            raise


def get_estate():
    sql_command = "select * from vwEstate"
    all_entries = run_sql(sql_command)
    return getResponse('estate', None, None, 1, all_entries)

def update_running_balance(BankName=None):
    running_balance_perBank = {}
    transactions = get_all_transactions(MinDate = '1900-01-01', BankName=BankName, oder_by = " order by Date")
    for t in transactions:
        print('t', t['Date'], t['Amount'])
        t['RunningBalance'] = running_balance_perBank.get(t['BankName'], 0) + t['Amount']
        update_transaction(transaction_id=t['id'], RunningBalance =  t['RunningBalance'] )
        running_balance_perBank[t['BankName']] = t['RunningBalance']