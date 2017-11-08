from flask import Flask
from flask_cors import CORS
from server.dto.data_server import distinct_bankAccounts, running_balance, amount_by_subcategory, amount_by_year_month_and_subcategory, distinct_years, distinct_types, distinct_categories, distinct_subCategories
from flask import request
from server.dto.transaction_management import get_transactions, save_transaction
from server.dto.category_management import get_categories, save_category, delete_category

app = Flask(__name__)
CORS(app)

@app.route('/categories/', methods=['POST'])
def post_categories():
    return app.make_response(
        save_category(request.form['id'], request.form['category'], request.form['description']))

@app.route('/transactions/', methods=['POST'])
def post_transactions():
    return app.make_response(
        save_transaction(request.form['id'], request.form['category'], request.form['SubCategory']))

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category_id(id):
    return app.make_response(delete_category(id))

def get_filters(request):
    yearFilter = request.args.get('year_filter')
    typeFilter = request.args.get('type_filter')
    categoryFilter = request.args.get('category_filter')
    subcategoryFilter = request.args.get('subcategory_filter')
    accountFilters = request.args.get('account_filters')
    return yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters

@app.route('/getAmountBySubCategory/', methods=['GET'])
def get_amount_by_subcategory():
    yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters = get_filters(request)
    return app.make_response(amount_by_subcategory(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters))

@app.route('/getRunningBalance/', methods=['GET'])
def get_running_balance():
    yearFilter = request.args.get('year_filter')
    accountFilters = request.args.get('account_filters')
    return app.make_response(running_balance(yearFilter, accountFilters))

@app.route('/getAmountByYearMonthAndSubCategory/', methods=['GET'])
def get_amount_by_subcategory2():
    yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters = get_filters(request)
    return app.make_response(amount_by_year_month_and_subcategory(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters))

@app.route('/getDistinctYears/', methods=['GET'])
def get_distinct_years():
    yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters = get_filters(request)
    return app.make_response(distinct_years(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters))

@app.route('/getDistinctTypes/', methods=['GET'])
def get_distinct_types():
    yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters = get_filters(request)
    return app.make_response(distinct_types(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters))

@app.route('/getDistinctCategories/', methods=['GET'])
def get_distinct_categories():
    yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters = get_filters(request)
    return app.make_response(distinct_categories(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters))

@app.route('/getDistinctSubCategories/', methods=['GET'])
def get_distinct_subCategories():
    yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters = get_filters(request)
    return app.make_response(distinct_subCategories(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters))

@app.route('/getDistinctBankAccounts/', methods=['GET'])
def get_distinct_bankAccounts():
    yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters = get_filters(request)
    return app.make_response(distinct_bankAccounts(yearFilter, typeFilter, categoryFilter, subcategoryFilter, accountFilters))

def getParams(request):
    sort_params = request.args.get('sort')
    sort = None
    sort_order = None
    if sort_params is not None:
        sort_params = sort_params.split('|')
        sort = sort_params[0]
        sort_order = sort_params[1]
    filter_param = request.args.get('filter')
    page_number = request.args.get('page')
    per_page = request.args.get('per_page')
    return sort, sort_order, filter_param, page_number, per_page


@app.route('/categories/', methods=['GET'])
def categories():
    sort, sort_order, filter_param, page_number, per_page = getParams(request)
    return app.make_response((get_categories(sort, sort_order, filter_param, page_number, per_page ), 200))

@app.route('/transactions/', methods=['GET'])
def transactions():
    sort, sort_order, filter_param, page_number, per_page = getParams(request)
    return app.make_response((get_transactions(sort, sort_order, filter_param, page_number, per_page ), 200))