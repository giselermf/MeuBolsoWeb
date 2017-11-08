from server.dto.base import create_connection, getResponse
import json

def get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause = type_clause = category_clause = subcategory_clause = account_clause = '1=1'
    
    if yearFilter is not None:
        year_clause =  " year in (%s) " % (yearFilter)
    
    if typeFilter is not None:
        type_clause =  "type in (%s) " % (typeFilter)

    if categoryFilter is not None:
        category_clause =  "Category in (%s) " % (categoryFilter) 

    if subcategoryFilter is not None:
        subcategory_clause =  "SubCategory in (%s) " % (subcategoryFilter) 

    if accountFilters is not None:
        account_clause =  "BankName in (%s) " % (accountFilters) 
    
    return year_clause, type_clause, category_clause, subcategory_clause, account_clause

def amount_by_subcategory(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    sql_command = "SELECT SubCategory, sum(AmountEUR) as Total FROM Transactions where %s and %s and %s and %s and %s group by SubCategory" % (year_clause, type_clause, category_clause, subcategory_clause, account_clause)
    return run_sql_command('data', sql_command)
 
def amount_by_year_month_and_subcategory(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    sql_command = "SELECt Year||'/'||Month as [yearmonth], subcategory, sum(AmountEUR) as Total FROM Transactions where %s and %s and %s and %s and %s group by Year,Month,subcategory order by year, month" % (year_clause, type_clause, category_clause, subcategory_clause, account_clause)
    return run_sql_command('data', sql_command)

def running_balance(yearFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, None, None, None, accountFilters)
    sql_command = "SELECt BankName, Date, round(RunningBalance) as Total FROM Transactions where Day=1 and %s and %s order by 1,2" % (year_clause, account_clause)
    return run_sql_command('data', sql_command)

def run_sql_command(param_name, sql_command):
    print(sql_command)
    conn = create_connection()
    c = conn.cursor()
    conn = create_connection()
    print(sql_command)
    with conn:
        c = conn.cursor()
        c.execute(sql_command)
        return json.dumps({param_name: c.fetchall()})

def distinct_years(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    return run_sql_command("filter_year", "select distinct Year from Transactions where %s and %s and %s and %s order by 1" % (type_clause, category_clause, subcategory_clause, account_clause))

def distinct_types(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    return run_sql_command("filter_type", "select distinct Type from Transactions where %s and %s and %s and %s order by 1" % (year_clause, category_clause, subcategory_clause, account_clause))

def distinct_categories(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    return run_sql_command("filter_categories", "select distinct Category from Transactions where %s and %s and %s and %s order by 1" % (year_clause, type_clause, subcategory_clause, account_clause))

def distinct_subCategories(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    return run_sql_command("filter_subcategories", "select distinct SubCategory from Transactions where Subcategory is not null and %s and %s and %s and %s order by 1" % (year_clause, type_clause, category_clause, account_clause))

def distinct_bankAccounts(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    return run_sql_command("filter_bankAccounts", "SELECt distinct BankName FROM Transactions where %s and %s and %s and %s order by 1" % (year_clause, type_clause, category_clause, subcategory_clause))



