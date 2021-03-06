from server.app.models import Category, Transaction, Categorydescription, Account, PendingReconciliation, \
    TransactionsFilterSchema, CategorySchema, CategorydescriptionSchema, TransactionsSchema, PendingReconciliationSchema, \
    BudgetSchema, update_running_balance
from flask import make_response, request
from sqlalchemy import desc,  func, and_, extract
from sqlalchemy.orm.session import make_transient
from datetime import datetime
from server.process_data.processor import Processor
import math
import pandas as pd
from distutils.util import strtobool
import json
from . import main
from .. import db
from server.process_data.category_management import Categories

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

def _getFilterByCategory(query, category_type=None, category=None, subcategory=None, category_id=None):
    if category_id:
        query = query.filter( Transaction.category_id == category_id)
    else:
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
    return resp

@main.route('/getFilterTransactionData/', methods=['GET'])
def getFilterTransactionData():
    results = Transaction.query.join(Category).join(Account).filter(Account.Active==1).\
        with_entities(Account.BankName, Category.Type, Category.Category, Category.SubCategory).distinct()
    return _getResponse('data', None, None, None, TransactionsFilterSchema(many=True).dump(results).data)

@main.route('/getAllAccounts/', methods=['GET'])
def getAllAccounts():
    filter_param = request.args.get('filter')
    fromDate = toDate = types = active = None

    if filter_param is not None:
        filter_param = json.loads(filter_param)
        fromDate=filter_param.get('fromDate')
        toDate=filter_param.get('toDate')
        types =filter_param.get('type')
        active =filter_param.get('active')

    query = Transaction.query.join(Account).distinct(Transaction.BankName, Transaction.Currency).\
        with_entities(Transaction.BankName, Transaction.Currency)
    if fromDate:
        query = query.filter(Transaction.Date >= fromDate)
    if toDate:
        query = query.filter(Transaction.Date <= toDate)
    if types:
        query = query.filter(Account.Type.in_(types))
    if active:
        query = query.filter(Account.Active == bool(active))
    output =  TransactionsSchema(many=True).dump(query.all()).data
    return _getResponse('data', None, None, None, output)


def get_transaction_query(sort, sort_order, 
                                    category_type=None, category=None, subcategory=None,
                                    bankNames=None, fromDate=None, toDate=None, 
                                    fromAmount=None, toAmount=None, description=None, 
                                    accountTypes=None, category_id=None, exclude_budget=True):
    query = Transaction.query.join(Category).join(Account)
    query = _getSortClause(query, sort, sort_order)
    query = _getFilterByCategory(query, category_type, category, subcategory, category_id)
    
    if bankNames != None:
        query = query.filter( Transaction.BankName.in_(tuple(bankNames)) )
    elif exclude_budget:
        query = query.filter( Transaction.BankName != "Budget")
    if fromDate != None:
        query = query.filter( Transaction.Date >= fromDate)
    if toDate != None:
        query = query.filter( Transaction.Date <= toDate)
    if fromAmount != None:
        query = query.filter( Transaction.AmountEUR >= float(fromAmount))
    if toAmount != None:
        query = query.filter( Transaction.AmountEUR <= float(toAmount ))
    if description != None:
        query = query.filter( Transaction.Description.like("%"+description+"%") )
    if accountTypes != None:
        query = query.filter(Account.Type.in_(tuple(accountTypes)))

    # print(bankNames, fromDate, toDate, fromAmount, toAmount, description, accountTypes)
    # print('to', 'float', float(toAmount) , 'string', toAmount)
    # print('query', str(query))
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
            bankNames=filter_param.get('bankNames'), fromDate=filter_param.get('fromDate'), toDate=filter_param.get('toDate'), 
            fromAmount=filter_param.get('fromAmount'), toAmount=filter_param.get('toAmount'), description=filter_param.get('Description'),
            accountTypes=filter_param.get("accountTypes"), category_id=filter_param.get("category_id") )
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

def _get_category_id(typec, cateogry, subcategory):
    return Category.query.\
        filter(Category.Type == typec).\
        filter(Category.Category == cateogry).\
        filter(Category.SubCategory ==subcategory).first().id

@main.route('/transactions/', methods=['POST'])
def post_transactions():
    category_id = None
    transaction_id = request.form.get('transaction_id')
    if request.form.get('Date'):
        date = pd.to_datetime(request.form.get('Date')).date()
    if not request.form.get('category_id') and request.form.get('Type') and request.form.get('Category') and request.form.get('SubCategory'):
        category_id = _get_category_id(request.form.get('Type'), request.form.get('Category'), request.form.get('SubCategory'))
    elif request.form.get('category_id') :
        category_id = int(request.form.get('category_id'))

    if not transaction_id:     
        new = Transaction(
                Description=request.form.get('Description'), \
                TransactionNumber=request.form.get('TransactionNumber'), \
                Currency=request.form.get('Currency'), \
                Amount=float(request.form.get('Amount',0)), \
                AmountEUR=float(request.form.get('AmountEUR',0)), \
                Date=date, \
                category_id=category_id, \
                BankName = request.form.get('BankName'), \
                PaymentDate=date)
        db.session.add(new)
        db.session.commit()
        update_running_balance(new.BankName)
        return _getResponse('insert transaction', None, None, None, new.id)
    else:
        existing = Transaction.query.get(transaction_id)
        if float(request.form.get('Amount',0)) == 0: #delete
            print('delete', float(request.form.get('Amount',0)))
            db.session.delete(existing)
            db.session.commit()
            update_running_balance(existing.BankName)
            return _getResponse('deleted transaction', None, None, None, None)
        else: # update
            print('update', float(request.form.get('Amount',0)))
            existing.update(category_id=category_id, \
                            description=request.form.get('Description'), \
                            date = date, \
                            transaction_number=request.form.get('TransactionNumber'), \
                            amount=float(request.form.get('Amount',0) ))
            db.session.commit()
            update_running_balance(existing.BankName)
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
        Date=existing.Date, category_id=new_category_id, BankName = existing.account, PaymentDate=existing.PaymentDate)
    try:
        db.session.add(new)
        db.session.commit()
        update_running_balance(new.BankName)
        return _getResponse('splitTransaction', None, None, None, 'sucess')
    except:
        db.session.rollback()
        raise

@main.route('/getFilterData/', methods=['GET'])
def filter_data():
    query = Category.query.all()
    return _getResponse('data', None, None, None, CategorySchema(many=True).dump(query).data)

#CATEGORIE
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
        to_update.category_id=category_id
        to_update.Description = category_description
        db.session.commit()
        return _getResponse('category updated', None, None, None, category_id)

@main.route('/categories/<int:id>', methods=['DELETE'])
def delete_category_id(id):
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

    if request.args.get('Date'):
        date = pd.to_datetime(request.args.get('Date')).date()
    else:
        date = datetime.now()

    subq = db.session.query(
        func.max(Transaction.id).label('maxid')).join(Account, Account.BankName == Transaction.BankName).filter(Account.Active==1).filter(Transaction.Date <= date).\
        group_by(Transaction.BankName, Account.Type).subquery('t1')

    subq2 = db.session.query(Transaction).join(Account, Account.BankName == Transaction.BankName).join(
        subq,
        and_(
            Transaction.id == subq.c.maxid
        )
    ).with_entities(Transaction.id, Transaction.BankName, Account.Type, Transaction.Date, Transaction.RunningBalance).subquery('t2')

    query = db.session.query(Transaction).join(Account, Account.BankName == Transaction.BankName).join(
        subq2,
        and_(
            Transaction.id == subq2.c.id
        )).group_by(Transaction.BankName).with_entities(Transaction.BankName, Account.Type, Transaction.Date, Transaction.RunningBalance)
    
    # import pdb; pdb.set_trace()
    output =  TransactionsSchema(many=True).dump(query.all()).data
    return _getResponse('estate', None, None, None, output)

    
@main.route('/processData/', methods=['POST'])
def process_data():
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

@main.route('/updateCategories/', methods=['POST'])
def udpate_categories():
    try:
        categories = Categories()
        transactions = Transaction.query.filter(Transaction.categoryManuallyUpdated == 0).all()
        for t in transactions:
            if t.category_id != categories.get_category(t.Description):
                t.category_id = categories.get_category(t.Description)
        db.session.commit()
        return _getResponse('updateClassification', None, None, 1, 'ok')
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

