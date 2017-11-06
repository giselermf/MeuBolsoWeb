from server.dto.base import create_connection, getResponse
import json

def amount_by_category(yearFilter, typeFilter, categoryFilter, subcategoryFilter):
    conn = create_connection()
    c = conn.cursor()
    year_clause = type_clause = category_clause = subcategory_clause = '1=1'
    
    if yearFilter is not None:
        year_clause =  " year in (%s) " % (yearFilter) 
    
    if typeFilter is not None:
        type_clause =  "type in (%s) " % (typeFilter) 

    if categoryFilter is not None:
        category_clause =  "Category in (%s) " % (categoryFilter) 

    if subcategoryFilter is not None:
        subcategory_clause =  "SubCategory in (%s) " % (subcategoryFilter) 

    sql_comand = "SELECT Category, sum(AmountEUR) as Total FROM Transactions where %s and %s and %s and %s  group by Category" % (year_clause, type_clause, category_clause, subcategory_clause)
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