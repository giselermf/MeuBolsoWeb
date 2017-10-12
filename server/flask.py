from flask import Flask
from flask_cors import CORS
from server.dto.data_server import get_categories, save_category, delete_category, get_transactions, save_transaction, amount_by_category
from flask import request

app = Flask(__name__)
CORS(app)

@app.route('/categories/', methods=['POST'])
def post_categories():
    if request.method == 'POST':
        return app.make_response(
            save_category(request.form['id'], request.form['category'], request.form['description']))

@app.route('/transactions/', methods=['POST'])
def post_transactions():
    if request.method == 'POST':
        return app.make_response(
            save_transaction(request.form['id'], request.form['category'], request.form['SubCategory']))


@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category_id(id):
    return app.make_response(delete_category(id))


@app.route('/getAmountByCategory/', methods=['GET'])
def get_amount_by_category():
    return app.make_response(amount_by_category())
# query methods 

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