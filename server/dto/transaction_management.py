from server.dto.base import getResponse, getFilterByCategoryClause, getLimitClause, getSortClause
from server.database.database_connection import run_select, run_update

def get_transactions(sort, sort_order, filter_param, page_number, per_page):
    sql_command = "Select * from Transactions"
    sql_command += getFilterByCategoryClause(filter_param)
    sql_command += getSortClause(sort, sort_order)
    sql_command += getLimitClause(page_number, per_page)
    all_entries = run_select(sql_command)
    total_records = run_select('select count(*) as total from Transactions')[0]['total']
    return getResponse('transactions', total_records, per_page, page_number, all_entries)

def get_transaction(currency, bank_name, amount, date_str, description, transaction_number=None):
    sql_command = "SELECt * FROM Transactions where Currency='{0}' and bankname='{1}' and Amount={2} and Date_str={3}"\
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

def update_transaction_number(new_transaction_number, current_transaction_number, transaction_id):
    if new_transaction_number != '...' and new_transaction_number != None and new_transaction_number != current_transaction_number and len(new_transaction_number) < 16:
        run_update("update Transactions set TransactionNumber = ? where id = ? ", (new_transaction_number, transaction_id))

def update_transaction_category(id, category, sub_category):
    if id == '':
        return json.dumps({"data": 'fail'})
    else:
        sql_command = "update Transactions set SubCategory = ?, Category = ? where id = ?"
        return run_update(sql_command, (sub_category, category, int(id)))

