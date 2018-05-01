from server.database.database_connection import run_select
from server.dto.base import getResponse
import json

def get_budget(sort=None, sort_order=None, filter_param=None, page_number=None, per_page=None):
    all_entries = run_select("Select * from vwBudget order by Year, Month")
    total_records = run_select('select count(*) as total from vwBudget ')[0]['total']
    return getResponse('Budget', total_records, per_page, page_number, all_entries)
