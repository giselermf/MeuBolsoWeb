from server.database.database_connection import run_sql
from server.dto.base import getResponse

def get_investments():
    all_entries = run_sql("SELECT * FROM vwInvestment")
    total_records = run_sql('select count(*) as total from vwInvestment ')[0]['total']
    return getResponse('investments', total_records, 100, 0, all_entries)

