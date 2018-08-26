from server.database.database_connection import run_sql
from server.dto.base import getResponse
import json

def get_investments():
    all_entries = run_sql("SELECT BankName, date(Date) as Date, round(RunningBalance,2) as RunningBalance FROM vwInvestment")
    total_records = run_sql('select count(*) as total from vwInvestment ')[0]['total']
    return getResponse('investments', total_records, 100, 0, all_entries)

def get_savings_accounts():
    all_entries = run_sql("Select * from vwSavingsAccounts")
    return json.dumps(all_entries)