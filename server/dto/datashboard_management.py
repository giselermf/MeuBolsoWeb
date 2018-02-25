from server.database.database_connection import run_select

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
    return run_select(sql_command, 'data')
 
def amount_by_year_month_and_subcategory(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    sql_command = "SELECt Year||'/'||Month as [yearmonth], subcategory, sum(AmountEUR) as Total FROM Transactions where %s and %s and %s and %s and %s group by Year,Month,subcategory order by year, month" % (year_clause, type_clause, category_clause, subcategory_clause, account_clause)
    return run_select(sql_command, 'data')

def running_balance(yearFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, None, None, None, accountFilters)
    sql_command = "SELECt BankName, Date, round(RunningBalance) as Total FROM Transactions where Day=1 and %s and %s order by 1,2" % (year_clause, account_clause)
    return run_select(sql_command, 'data')

def distinct_years(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    sql_command = "select distinct Year from Transactions where %s and %s and %s and %s order by 1" % (type_clause, category_clause, subcategory_clause, account_clause)
    return run_select(sql_command, "filter_year")

def distinct_types(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    sql_command = "select distinct Type from Transactions where %s and %s and %s and %s order by 1" % (year_clause, category_clause, subcategory_clause, account_clause)
    return run_select(sql_command, "filter_type")

def distinct_categories(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    sql_command =  "select distinct Category from Transactions where %s and %s and %s and %s order by 1" % (year_clause, type_clause, subcategory_clause, account_clause)
    return run_select(sql_command, "filter_categories")

def distinct_subCategories(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    sql_command = "select distinct SubCategory from Transactions where Subcategory is not null and %s and %s and %s and %s order by 1" % (year_clause, type_clause, category_clause, account_clause)
    return run_select(sql_command, "filter_subcategories")

def distinct_bankAccounts(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters):
    year_clause, type_clause, category_clause, subcategory_clause, account_clause = get_where_clauses(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters)
    sql_command = "SELECt distinct BankName FROM Transactions where %s and %s and %s and %s order by 1" % (year_clause, type_clause, category_clause, subcategory_clause)
    return run_select(sql_command, "filter_bankAccounts")



