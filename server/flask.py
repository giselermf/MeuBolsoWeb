from flask import Flask
from flask_cors import CORS
from flask import request
from server.dto.transaction_management import update_transaction, get_transactions_filtered, get_filter_transaction_data, split_transaction, get_estate, save_transfer
#from server.dto.category_management import get_categories, save_category, delete_category, get_filter_data, get_category_id
from server.process_data.processor import Processor
from server.process_data.category_management import Categorization
from server.dto.budget_management import get_budget, update_budget, get_cashFlow, get_RunningBalance
from server.dto.investment_management import get_investments, get_savings_accounts
import json

app = Flask(__name__)
CORS(app)

# @app.route('/processData/', methods=['GET'])
# def process_data():
#     folder = request.args.get('folder')
#     Processor(folder).process()
#     return app.make_response('ok')

@app.route('/recategorize/', methods=['GET'])
def recategorize():
    Categorization().run()
    return app.make_response('ok')

# @app.route('/categories/', methods=['POST'])
# def post_categories():
#     print(request.form)
#     return app.make_response (
#         save_category(request.form['id'], request.form['selectedCategoryid'], request.form['description'])
#         )

# @app.route('/categories/<int:id>', methods=['DELETE'])
# def delete_category_id(id):
#     return app.make_response(delete_category(id))

# @app.route('/categories/', methods=['GET'])
# def categories():
#     sort, sort_order, filter_param, page_number, per_page = getParams(request)
#     if filter_param is not None:
#         filter_param = json.loads(filter_param)
#     return app.make_response(( get_categories(sort, sort_order, filter_param, page_number, per_page ), 200))


# @app.route('/getFilterData/', methods=['GET'])
# def filter_data():
#     return app.make_response(get_filter_data())

# TRANSACTIONS
# @app.route('/getFilterTransactionData/', methods=['GET'])
# def getFilterTransactionData():
#     return app.make_response(get_filter_transaction_data())

# @app.route('/transactionsFiltered/', methods=['GET'])
# def transactionsFiltered():
#     sort, sort_order, filter_param, page_number, per_page = getParams(request)
#     if filter_param is not None:
#         filter_param = json.loads(filter_param)
#     return app.make_response((get_transactions_filtered(sort, sort_order, filter_param, page_number, per_page ), 200))

# @app.route('/transactions/', methods=['POST'])
# def post_transactions():
#     transaction_id = request.form.get('transaction_id')
#     Description = request.form.get('Description')
#     TransactionNumber = request.form.get('TransactionNumber')
#     Currency = request.form.get('Currency')
#     Amount = request.form.get('Amount')
#     BankName = request.form.get('BankName')
#     AmountEUR = request.form.get('AmountEUR')
#     RunningBalance = request.form.get('RunningBalance')
#     Date = request.form.get('Date')
#     if request.form.get('category_id') is None:
#         category_id = get_category_id(request.form.get('Type'), request.form.get('Category'), request.form.get('SubCategory'))
#     else:
#         category_id = request.form.get('category_id')
#     return app.make_response(
#         update_transaction(transaction_id, Description ,TransactionNumber ,Currency ,Amount , BankName ,AmountEUR , Date , category_id, RunningBalance))

# @app.route('/splitTransaction/', methods=['POST'])
# def split_transactions():
#     return app.make_response(
#         split_transaction(transactionId=request.form['transaction_id'], newCategoryId=request.form['new_category_id'], newAmountEUR=request.form['new_amount_EUR']))

# def getParams(request): 
#     sort_params = request.args.get('sort')
#     sort = None
#     sort_order = 'asc'
#     if sort_params is not None:
#         sort_params = sort_params.split('|')
#         sort = sort_params[0]
#         sort_order = sort_params[1]
#     filter_param = request.args.get('filter')
#     page_number = request.args.get('page')
#     per_page = request.args.get('per_page')
#     return sort, sort_order, filter_param, page_number, per_page

# @app.route('/transfer/', methods=['POST'])
# def post_transfer():
#     transaction_id = request.form.get('transaction_id')
#     TransactionNumber = request.form.get('TransactionNumber')
#     Currency = request.form.get('Currency')
#     Amount = request.form.get('Amount')
#     toSelectedBank = request.form.get('toSelectedBank')
#     AmountEUR = request.form.get('AmountEUR')
#     Date = request.form.get('Date')
#     category_id = get_category_id('Transfer','Transfer','Transfer')
#     oldTransferId = request.form.get('oldTransferId')
#     return app.make_response(
#         save_transfer(transaction_id ,TransactionNumber ,Currency ,Amount , toSelectedBank ,AmountEUR , Date , category_id, oldTransferId))


# # BUDGET
# @app.route('/budget/', methods=['GET'])
# def getBudget():
#     filter_param = request.args.get('filter')
#     if filter_param is not None:
#         filter_param = json.loads(filter_param)
#     return app.make_response(get_budget(filter_param))

# @app.route('/budget/', methods=['POST'])
# def post_budget():
#     return app.make_response(
#         update_budget(id=request.form['id'], CategoryId=request.form['CategoryId'], \
#         Value=request.form['Value'], Day=request.form['Day'], Month=request.form['Month'], Year=request.form['Year']))

# # CASH_FLOW
# @app.route('/cashFlow/', methods=['GET'])
# def getCashFlow():
#     filter_param = request.args.get('filter')
#     if filter_param is not None:
#         filter_param = json.loads(filter_param)
#     return app.make_response(get_cashFlow(filter_param))

# @app.route('/RunningBalance/', methods=['GET'])
# def getRunningBalance():
#     filter_param = request.args.get('filter')
#     if filter_param is not None:
#         filter_param = json.loads(filter_param)
#     return app.make_response(get_RunningBalance(filter_param))

# #INVESTMENT
# @app.route('/Investment/', methods=['GET'])
# def getInvestment():
#     return app.make_response(get_investments())

# @app.route('/SavingsAccounts/', methods=['GET'])
# def getSavingsAccounts():
#     return app.make_response(get_savings_accounts())


# #ESTATE
# @app.route('/estate/', methods=['GET'])
# def getEstate():
#     return app.make_response(get_estate())