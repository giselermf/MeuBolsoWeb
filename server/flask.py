from flask import Flask
from flask_cors import CORS
from flask import request
from server.dto.transaction_management import update_transaction, get_filter_data, get_transactions_filtered
from server.dto.category_management import get_categories, save_category, delete_category
from server.process_data.processor import Processor
from server.process_data.category_management import Categorization
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
    return app.make_response(
        save_category(request.form['id'], request.form['category'], request.form['description']))

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category_id(id):
    return app.make_response(delete_category(id))

@app.route('/categories/', methods=['GET'])
def categories():
    sort, sort_order, filter_param, page_number, per_page = getParams(request)
    return app.make_response((get_categories(sort, sort_order, filter_param, page_number, per_page ), 200))

# TRANSACTIONS

@app.route('/getFilterData/', methods=['GET'])
def filter_data():
    return app.make_response(get_filter_data())

@app.route('/transactionsFiltered/', methods=['GET'])
def transactionsFiltered():
    sort, sort_order, filter_param, page_number, per_page = getParams(request)
    print('***', filter_param)
    if filter_param is not None:
        filter_param = json.loads(filter_param)
    return app.make_response((get_transactions_filtered(sort, sort_order, filter_param, page_number, per_page ), 200))

@app.route('/transactions/', methods=['POST'])
def post_transactions():
    return app.make_response(
        update_transaction(id=request.form['id'], category=request.form['category'], sub_category=request.form['SubCategory']))

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
