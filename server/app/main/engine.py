from server.app.models import Category, Transaction, Categorydescription, Account, \
    update_running_balance, PendingReconciliation, \
    TransactionsFilterSchema, CategorySchema, CategorydescriptionSchema, TransactionsSchema, PendingReconciliationSchema, BudgetSchema
from flask import make_response, request
from sqlalchemy import desc,  func, and_, extract
from datetime import datetime
from server.process_data.processor import Processor
import math
import pandas as pd
from distutils.util import strtobool
import json
from . import main
from .. import db

def _getLimitClause(query, page_number, per_page):
    if page_number is not None and per_page is not None:
        page_number = int(page_number)
        per_page = int(per_page)
        start = (per_page * (page_number-1))
        return query.slice(start, start+per_page)
    return query

def _getSortClause(query, sort, sort_order):
    if sort is not None and sort != '':
        if sort_order == "desc":
            return query.order_by(desc(sort))
        else:
            return query.order_by(sort)
    return query

def _getFilterByCategory(query, category_type=None, category=None, subcategory=None,):
    if category_type:
        query = query.filter( Category.Type == category_type )
    if category:
        query = query.filter( Category.Category == category )
    if subcategory:
        query = query.filter( Category.SubCategory == subcategory )
    return query

def _getParams(request): 
    sort_params = request.args.get('sort')
    sort = None
    sort_order = 'asc'
    print('sort_params',sort_params)
    if sort_params is not None:
        sort_params = sort_params.split('|')
        sort = sort_params[0]
        if len(sort_params) > 1:
            sort_order = sort_params[1]
        else:
            sort_order = "asc"
    filter_param = request.args.get('filter')
    page_number = request.args.get('page')
    per_page = request.args.get('per_page')
    return sort, sort_order, filter_param, page_number, per_page

def _getResponse(url, total_records, per_page, page_number, all_entries): 
    total_records = 0 if total_records is None else int(total_records)
    per_page = 1 if per_page is None else int(per_page)
    page_number = 0 if page_number is None else int(page_number)
    response = {}
    response['per_page'] = per_page
    response['current_page'] = page_number
    response['last_page'] = math.ceil(total_records/per_page)
    response['total'] = total_records
    response['next_page_url'] = "%s?page=%s" % (url, page_number+1)
    response['prev_page_url'] = "%s?page=%s" % (url, page_number-1)
    response['from'] = int ((page_number -1) * per_page + 1) 
    response['to'] = response['from'] + per_page
    response['data'] = all_entries
    resp = make_response(json.dumps(response))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, PUT, POST, DELETE"
    resp.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    return resp

@main.route('/getFilterTransactionData/', methods=['GET'])
def getFilterTransactionData():
    results = Transaction.query.join(Category).join(Account).filter(Account.Active==1).\
        with_entities(Account.BankName, Category.Type, Category.Category, Category.SubCategory).distinct()
    return _getResponse('data', None, None, None, TransactionsFilterSchema(many=True).dump(results).data)

@main.route('/getAllAccounts/', methods=['GET'])
def getAllAccounts():
    filter_param = request.args.get('filter')
    fromDate=None
    toDate=None
    if filter_param is not None:
        filter_param = json.loads(filter_param)
        fromDate=filter_param.get('fromDate')
        toDate=filter_param.get('toDate')

    query = Transaction.query.distinct(Transaction.BankName, Transaction.Currency).\
        with_entities(Transaction.BankName, Transaction.Currency).filter(Transaction.BankName != "Budget")
    if fromDate:
        query = query.filter( Transaction.Date >= fromDate)
    if toDate:
        query = query.filter( Transaction.Date <= toDate)
    output =  TransactionsSchema(many=True).dump(query.all()).data
    return _getResponse('data', None, None, None, output)


def get_transaction_query(sort, sort_order, 
                                    category_type=None, category=None, subcategory=None,
                                    bankName=None, fromDate=None, toDate=None, 
                                    fromAmount=None, toAmount=None, description=None, 
                                    exclude_budget=True):
    query = Transaction.query.join(Category).join(Account)
    query = _getSortClause(query, sort, sort_order)
    query = _getFilterByCategory(query, category_type, category, subcategory)
    
    if bankName:
        query = query.filter( Transaction.BankName == bankName)
    elif exclude_budget:
        query = query.filter( Transaction.BankName != "Budget")
    if fromDate:
        query = query.filter( Transaction.Date >= fromDate)
    if toDate:
        query = query.filter( Transaction.Date <= toDate)
    if fromAmount:
        query = query.filter( Transaction.AmountEUR >= float(fromAmount))
    if toAmount:
        query = query.filter( Transaction.AmountEUR <= float(toAmount ))
    if description:
        query = query.filter( Transaction.Description.like("%"+description+"%") )
    return query


@main.route('/transactionsFiltered/', methods=['GET'])
def transactionsFiltered():
    sort, sort_order, filter_param, page_number, per_page = _getParams(request)
    total = 0
    output = []
    if filter_param is not None:
        filter_param = json.loads(filter_param)
        query = get_transaction_query( sort=sort, sort_order=sort_order, 
            category_type=filter_param.get('type'), category=filter_param.get('category'), subcategory=filter_param.get('subcategory'),
            bankName=filter_param.get('bankName'), fromDate=filter_param.get('fromDate'), toDate=filter_param.get('toDate'), 
            fromAmount=filter_param.get('fromAmount'), toAmount=filter_param.get('toAmount'), description=filter_param.get('Description'), 
            exclude_budget=True)
        total = len(query.all())
        query = _getLimitClause(query, page_number, per_page)
        output =  TransactionsSchema(many=True).dump(query.all()).data
    return _getResponse('transactions', total, per_page, page_number, output)

@main.route('/deleteTransaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    print('in delete transaction')
    to_be_deleted = Transaction.query.filter(Transaction.id == transaction_id).first()
    db.session.delete(to_be_deleted)
    db.session.commit()
    return _getResponse('transaction deleted', None, None, None, transaction_id)

@main.route('/transactions/', methods=['POST'])
def post_transactions():
    transaction_id = request.form.get('transaction_id')
    if request.form.get('Date'):
        date = pd.to_datetime(request.form.get('Date')).date()
    if not request.form.get('category_id') and request.form.get('Type') and request.form.get('Category') and request.form.get('SubCategory'):
        category_id = Category.query.\
                                    filter(Category.Type == request.form.get('Type')).\
                                    filter(Category.Category == request.form.get('Category')).\
                                    filter(Category.SubCategory == request.form.get('SubCategory')).first().id
    elif request.form.get('category_id') :
        category_id = int(request.form.get('category_id'))

    if not transaction_id:     
        new = Transaction(
                Description=request.form.get('Description'), \
                TransactionNumber=request.form.get('TransactionNumber'), \
                Currency=request.form.get('Currency'), \
                Amount=float(request.form.get('Amount',0)), \
                AmountEUR=float(request.form.get('AmountEUR',0)), \
                RunningBalance=request.form.get('RunningBalance'), \
                Date=date, \
                category_id=category_id, \
                BankName = request.form.get('BankName'), \
                PaymentDate=date)
        db.session.add(new)
        db.session.commit()
        return _getResponse('insert transaction', None, None, None, new.id)
    else:
        existing = Transaction.query.get(transaction_id)
        if float(request.form.get('Amount',0)) == 0: #delete
            db.session.delete(existing)
            db.session.commit()
            return _getResponse('deleted transaction', None, None, None, None)
        else: # update
            existing.update(category_id=category_id, \
                            transaction_number=request.form.get('TransactionNumber'), \
                            running_balance=request.form.get('RunningBalance'), \
                            amount=float(request.form.get('Amount',0)), \
                            amountEUR=float(request.form.get('AmountEUR',0)))
            db.session.commit()
            return _getResponse('update transaction', None, None, None, existing.id)
     
@main.route('/splitTransaction/', methods=['POST'])
def split_transactions():
    original_transaction_id = request.form['transaction_id']
    new_category_id = request.form['new_category_id']
    new_amount_eur =request.form['new_amount_EUR']
    existing = Transaction.query.filter_by(id=original_transaction_id ).first()
    existing.AmountEUR = float(existing.AmountEUR) - float(new_amount_eur)
    existing.RunningBalance = float(existing.RunningBalance) - float(new_amount_eur)
    new = Transaction(
        Description="Split", TransactionNumber=existing.TransactionNumber, Currency=existing.Currency, \
        Amount=0, AmountEUR=float(new_amount_eur), RunningBalance=float(existing.RunningBalance) + float(new_amount_eur), \
        Date=existing.Date, category_id=new_category_id, account = existing.account, PaymentDate=existing.PaymentDate)
    try:
        db.session.add(new)
        db.session.commit()
        return _getResponse('splitTransaction', None, None, None, 'sucess')
    except:
        db.session.rollback()
        raise

@main.route('/addFutureTransactions/', methods=['POST'])
def add_future_transactions():
    new_transactions = []
    try:
        date = pd.to_datetime(request.form['fromDate']).date()
        for x in range(0, int(request.form['numberOccurrencies'])):
            new = Transaction(  Description = request.form['Description'],
                                TransactionNumber = 'Future',
                                Currency= request.form['Currency'],
                                Amount= float(request.form.get('AmountEUR',0)),
                                AmountEUR= float(request.form.get('AmountEUR',0)),
                                Date= date, 
                                PaymentDate= date,
                                category_id = request.form.get('category_id'),
                                BankName = request.form.get('BankName') )
            new_transactions.append(new)
            db.session.add(new)
            if request.form['frequency'] == "Monthly":
                date =  date + pd.DateOffset(months=1)
            elif request.form['frequency'] == "Weekly":
                date = date + pd.DateOffset(weeks=1)
            elif request.form['frequency'] == "Quartely":
                date = date + pd.DateOffset(months=3)
            elif request.form['frequency'] == "Yearly":
                date = date + pd.DateOffset(years=1)
        db.session.commit()
        update_running_balance(request.form['BankName'])
        return _getResponse('addFutureTransactions', None, None, None, TransactionsSchema(many=True).dump(new_transactions).data)
    except:
        db.session.rollback()
        raise

@main.route('/getFilterData/', methods=['GET'])
def filter_data():
    query = Category.query.all()
    return _getResponse('data', None, None, None, CategorySchema(many=True).dump(query).data)

@main.route('/categories/', methods=['POST'])
def post_categories():
    category_description_id = request.form.get('id')
    category_id = request.form.get('selectedCategoryid')
    category_description = request.form.get('description')
    if category_description_id == '' or category_description_id is None:
        new = Categorydescription(Description=category_description, category_id=category_id)
        db.session.add(new)
        db.session.commit()
        return _getResponse('category new', None, None, None, new.id)
    else:
        to_update = Categorydescription.query.filter_by(id=category_description_id).first()
        to_update.Description = category_description
        db.session.commit()
        return _getResponse('category updated', None, None, None, category_id)

@main.route('/categories/<int:id>', methods=['DELETE'])
def delete_category_id(id):
    print('in delete categories')
    to_be_deleted = Categorydescription.query.filter_by(id=id).first()
    db.session.delete(to_be_deleted)
    db.session.commit()
    return _getResponse('category deleted', None, None, None, id)

@main.route('/categories/', methods=['GET'])
def categories():
    sort, sort_order, filter_param, page_number, per_page = _getParams(request)
    query = Categorydescription.query.join(Category)
    total = len(query.all())
    query = _getSortClause(query, sort, sort_order)
    if filter_param is not None:
        filter_param = json.loads(filter_param)
        query = _getFilterByCategory(query, filter_param.get('type'), filter_param.get('category'), filter_param.get('subcategory'))
        if filter_param.get('description'):
            query = query.filter( Categorydescription.Description.like("%"+filter_param.get('description')+"%") )
    query = _getLimitClause(query, page_number, per_page)
    output =  CategorydescriptionSchema(many=True).dump(query.all()).data
    return _getResponse('category', total, per_page, page_number, output)

#ESTATE
@main.route('/estate/', methods=['GET'])
def getEstate():
    subq = db.session.query(
        Transaction.BankName,
        func.max(Transaction.Date).label('maxdate')).join(Account).filter(Account.Active==1).filter(Transaction.Date <= datetime.now()).\
        group_by(Transaction.BankName).subquery('t1')

    subq2 = db.session.query(Transaction).join(
        subq,
        and_(
            Transaction.BankName == subq.c.BankName,
            Transaction.Date == subq.c.maxdate
        )
    ).subquery('t2')

    query = db.session.query(Transaction).join(
        subq2,
        and_(
            Transaction.BankName == subq2.c.BankName,
            Transaction.Date == subq2.c.Date
        )).group_by(Transaction.BankName).with_entities(Transaction.BankName, Transaction.Date, Transaction.RunningBalance)

    output =  TransactionsSchema(many=True).dump(query.all()).data
    return _getResponse('estate', None, None, None, output)

# BUDGET
@main.route('/budget/', methods=['GET'])
def getBudget():
    filter_param = request.args.get('filter')
    if filter_param is not None:
        filter_param = json.loads(filter_param)

    budget_query = get_transaction_query( sort='Date', sort_order='desc', 
            bankName='Budget', fromDate=filter_param.get('fromDate'), toDate=filter_param.get('toDate'))
    actuals_query = get_transaction_query( sort='Date', sort_order='desc', 
            fromDate=filter_param.get('fromDate'), toDate=filter_param.get('toDate'))

    q2 = actuals_query.with_entities(
        extract('month', Transaction.Date).label('Month'), extract('year', Transaction.Date).label('Year'), 
        Category.id.label('category_id'), Category.Type, Category.Category, Category.SubCategory, func.sum(Transaction.AmountEUR).label('Actuals')).\
        group_by(extract('month', Transaction.Date), extract('year', Transaction.Date), Category.id, Category.Type, Category.Category, Category.SubCategory).\
        subquery('actuals')
        
    final_query = budget_query.outerjoin(
            q2,
            and_(
                extract('month', Transaction.Date) == q2.c.Month,
                extract('year', Transaction.Date)== q2.c.Year,
                Transaction.category_id == q2.c.category_id
            )).with_entities(
        Transaction.id,
        extract('day', Transaction.Date).label('Day'), extract('month', Transaction.Date).label('Month'), extract('year', Transaction.Date).label('Year'),
        Transaction.AmountEUR.label('Amount'), Category.id.label('category_id'), 
        Category.Type.label('Type'), Category.Category.label('Category'), Category.SubCategory.label('SubCategory'), q2.c.Actuals.label('Actuals')
    )
    
    output =  BudgetSchema(many=True).dump(final_query.all()).data
    return _getResponse('Budget', None, None, 1, output)

@main.route('/budget/', methods=['POST'])
def post_budget():
    transaction_id=request.form['id']
    category_id=request.form['CategoryId']
    value=request.form['Value']
    day=request.form['Day']
    month=request.form['Month']
    year=request.form['Year']
    date = datetime(year= int(year), month= int(month), day= int(day))

    if not transaction_id:     
        new = Transaction(
            Description='Budget entry', TransactionNumber=None, Currency='EUR', \
            Amount=value, AmountEUR=value, RunningBalance=0, \
            Date=date, category_id=category_id, account = 'Budget', PaymentDate=date)
        db.session.add(new)
        db.session.commit()
        return _getResponse('insert budget', None, None, None, new.id)
    else:
        existing = Transaction.get(transaction_id)
        if amount == 0: #delete
            db.session.delete(existing)
            db.session.commit()
            return _getResponse('deleted budget', None, None, None, new.id)
        else: # update
            existing.update(category_id=category_id, \
                 amount=value, amountEUR=value)
            db.session.commit()
            return _getResponse('update budget', None, None, None, new.id)


#INVESTMENT
@main.route('/Investment/', methods=['GET'])
def getInvestment():
    query = db.session.query(
        Transaction.BankName,
        func.max(Transaction.id).label('max_transaction_id')
    ).group_by(Transaction.BankName).join(Account).filter(Account.Active == 1).filter(Account.Type=='Savings').\
    with_entities(Transaction.Date, Transaction.RunningBalance, Transaction.BankName)

    total = len(query.all())
    output =  TransactionsSchema(many=True).dump(query.all()).data
    return _getResponse('investments', total, 100, 0, output)
    
@main.route('/processData/', methods=['POST'])
def process_data():
    print('here', request.form.__dict__)
    folder = request.form['folder']
    Processor(folder).process()
    return pending_reconciliation()

@main.route('/updateRunningBalance/', methods=['GET'])
def udpate_runnning_balance():
    try:
        accounts = Account.query.all()
        for a in accounts:
            update_running_balance(a.BankName)
        return _getResponse('updateRunningBalance', None, None, 1, 'ok')
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

#PENDING RECONCILIATION

@main.route('/PendingReconciliationTransactions/', methods=['GET'])
def pending_reconciliation():
    t1 = db.aliased(Transaction)
    t2 = db.aliased(Transaction)

    query = PendingReconciliation.query.join(t1, PendingReconciliation.transaction_id1==t1.id).\
        join(t2, PendingReconciliation.transaction_id2==t2.id)

    total = len(query.all())
    output = PendingReconciliationSchema(many=True).dump(query.all()).data
    return _getResponse('pendingReconciliation', total, 100, 0, output)

@main.route('/ProcessReconciliation/', methods=['POST'])
def process_reconciliation():
    reconciliation_id = int(request.form['reconciliation_id'])
    transaction1_id = int(request.form['transaction1_id'])
    transaction1_keep = strtobool(request.form['transaction1_keep'])
    transaction2_id = int(request.form['transaction2_id'])
    transaction2_keep = strtobool(request.form['transaction2_keep'])
    print('ProcessReconciliation', reconciliation_id, transaction1_id, transaction1_keep, transaction2_id, transaction2_keep)
    try:
        if not transaction1_keep:
            db.session.delete(Transaction.query.get(transaction1_id))
        if not transaction2_keep:
            db.session.delete(Transaction.query.get(transaction2_id))

        db.session.delete(PendingReconciliation.query.get(reconciliation_id))

        db.session.commit()
        return _getResponse('ProcessReconciliation', None, None, None, reconciliation_id)
    except:
        db.session.rollback()
        raise

