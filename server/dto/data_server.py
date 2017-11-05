from server.dto.base import create_connection, getResponse
import json

#def dict_factory(cursor, row):
#    d = {}
#    for idx, col in enumerate(cursor.description):
#        d[col[0]] = row[idx]
#    return d


def amount_by_category(yearFilter):
    conn = create_connection()
    c = conn.cursor()
    where_clause = ''
    if yearFilter is not None:
        where_clause =  "where year in (%s) " % (yearFilter) 
    sql_comand = "SELECT Category, sum(AmountEUR) as Total FROM Transactions %s group by Category" % (where_clause)
    print ('sql_comand', sql_comand)
    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute(sql_comand)
        all_entries = c.fetchall()
        return json.dumps({"data": all_entries})

def run_sql_command(param_name, sql_comand):
    conn = create_connection()
    c = conn.cursor()
    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute(sql_comand)
        return json.dumps({param_name: c.fetchall()})

def distinct_years():
    return run_sql_command("filter_year", "select distinct strftime('%Y',Date) as year from Transactions order by 1")

def distinct_types():
    return run_sql_command("filter_type", "select distinct Type from Transactions order by 1")

def distinct_categories():
    return run_sql_command("filter_categories", "select distinct Category from Transactions order by 1")

def distinct_subCategories():
    return run_sql_command("filter_subcategories", 
"select distinct SubCategory from Transactions where Subcategory is not null order by 1")