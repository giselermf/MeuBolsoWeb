from flask import Flask
from flask_cors import CORS
from flask import request
from server.dto.transaction_management import update_transaction, get_transactions_filtered, get_filter_transaction_data
from server.dto.category_management import get_categories, save_category, delete_category, get_filter_data
from server.process_data.processor import Processor
from server.process_data.category_management import Categorization
from server.dto.budget_management import get_budget, update_budget, get_cashFlow, get_RunningBalance

import json

app = Flask(__name__)
CORS(app)

@app.route('/processData/', methods=['GET'])
def process_data():
    folder = request.args.get('folder')
    Processor(folder).process()
    return app.make_response('ok')

@app.route('/recategorize/', methods=['GET'])
def recategorize():
    Categorization().run()
    return app.make_response('ok')

@app.route('/categories/', methods=['POST'])
def post_categories():
    print(request.form)
    return app.make_response (
        save_category(request.form['id'], request.form['selectedCategoryid'], request.form['description'])
        )

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category_id(id):
    return app.make_response(delete_category(id))

@app.route('/categories/', methods=['GET'])
def categories():
    sort, sort_order, filter_param, page_number, per_page = getParams(request)
    if filter_param is not None:
        filter_param = json.loads(filter_param)
    return app.make_response(( get_categories(sort, sort_order, filter_param, page_number, per_page ), 200))


@app.route('/getFilterData/', methods=['GET'])
def filter_data():
    return app.make_response(get_filter_data())

# TRANSACTIONS
@app.route('/getFilterTransactionData/', methods=['GET'])
def getFilterTransactionData():
    return app.make_response(get_filter_transaction_data())

@app.route('/transactionsFiltered/', methods=['GET'])
def transactionsFiltered():
    sort, sort_order, filter_param, page_number, per_page = getParams(request)
    if filter_param is not None:
        filter_param = json.loads(filter_param)
    return app.make_response((get_transactions_filtered(sort, sort_order, filter_param, page_number, per_page ), 200))

@app.route('/transactions/', methods=['POST'])
def post_transactions():
    return app.make_response(
        update_transaction(id=request.form['id'], category=request.form['category'], sub_category=request.form['SubCategory'], type=request.form['Type']))

def getParams(request):
    sort_params = request.args.get('sort')
    sort = None
    sort_order = 'asc'
    if sort_params is not None:
        sort_params = sort_params.split('|')
        sort = sort_params[0]
        sort_order = sort_params[1]
    filter_param = request.args.get('filter')
    page_number = request.args.get('page')
    per_page = request.args.get('per_page')
    return sort, sort_order, filter_param, page_number, per_page

# BUDGET
@app.route('/budget/', methods=['GET'])
def getBudget():
    filter_param = request.args.get('filter')
    if filter_param is not None:
        filter_param = json.loads(filter_param)
    return app.make_response(get_budget(filter_param))

@app.route('/budget/', methods=['POST'])
def post_budget():
    return app.make_response(
        update_budget(id=request.form['id'], CategoryId=request.form['CategoryId'], \
        Value=request.form['Value'], Month=request.form['Month'], Year=request.form['Year']))

# CASH_FLOW
@app.route('/cashFlow/', methods=['GET'])
def getCashFlow():
    filter_param = request.args.get('filter')
    if filter_param is not None:
        filter_param = json.loads(filter_param)
    return app.make_response(get_cashFlow(filter_param))

@app.route('/RunningBalance/', methods=['GET'])
def getRunningBalance():
    filter_param = request.args.get('filter')
    if filter_param is not None:
        filter_param = json.loads(filter_param)
    return app.make_response(get_RunningBalance(filter_param))