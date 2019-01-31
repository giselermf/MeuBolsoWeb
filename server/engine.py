from server.dto.models import db, app, Category, Transaction, Categorydescription, Account, update_insert_transaction
from flask import Flask, request
from flask_marshmallow import Marshmallow, fields
from marshmallow.fields import Int, String, Float
import json
from sqlalchemy import desc,  func, and_, extract
from datetime import datetime
from server.process_data.processor import Processor
import math

ma = Marshmallow(app)

class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category

class CategorydescriptionSchema(ma.ModelSchema):
    class Meta:
        model = Categorydescription
    category = ma.Nested(CategorySchema)

class AccountSchema(ma.ModelSchema):
    class Meta:
        model = Account     

class TransactionsSchema(ma.ModelSchema):
    class Meta:
        model = Transaction
    Month = Int(dump_only=True)
    Year = Int(dump_only=True)
    Day = Int(dump_only=True)
    Type = String(dump_only=True)
    Category = String(dump_only=True)
    SubCategory = String(dump_only=True)
    BankName = String(dump_only=True)
    Active = String(dump_only=True)

class BudgetSchema(ma.ModelSchema):
    id = Int(dump_only=True)
    Month = Int(dump_only=True)
    Year = Int(dump_only=True)
    Day = Int(dump_only=True)
    Type = String(dump_only=True)
    Category = String(dump_only=True)
    SubCategory = String(dump_only=True)
    category_id = Int(dump_only=True)
    transactions_id = Int(dump_only=True)
    Actuals= Float(dump_only=True)
    Amount= Float(dump_only=True)

class TransactionsFilterSchema(ma.Schema):
    class Meta:
        fields = ('BankName', 'Type', 'Category', 'SubCategory')

def getLimitClause(query, page_number, per_page):
    if page_number is not None and per_page is not None:
        page_number = int(page_number)
        per_page = int(per_page)
        start = (per_page * (page_number-1))
        return query.slice(start, start+per_page)
    return query

def getSortClause(query, sort, sort_order):
    if sort is not None and sort != '':
        if sort_order == "desc":
            return query.order_by(desc(sort))
        else:
            return query.order_by(sort)
    return query

def getFilterByCategory(query, category_type=None, category=None, subcategory=None,):
    if category_type:
        query = query.filter( Category.Type == category_type )
    if category:
        query = query.filter( Category.Category == category )
    if subcategory:
        query = query.filter( Category.SubCategory == subcategory )
    return query

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

def getResponse(url, total_records, per_page, page_number, all_entries): 
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
    return json.dumps(response)

@app.route('/getFilterTransactionData/', methods=['GET'])
def getFilterTransactionData():
    results = Transaction.query.join(Category).join(Account).filter(Account.Active==1).\
        with_entities(Account.BankName, Category.Type, Category.Category, Category.SubCategory).distinct()
    return getResponse('data', None, None, None, TransactionsFilterSchema(many=True).dump(results).data)

def get_transaction_query(sort, sort_order, 
                                    category_type=None, category=None, subcategory=None,
                                    bankName=None, fromDate=None, toDate=None, 
                                    fromAmount=None, toAmount=None, description=None, 
                                    exclude_budget=True):
    query = Transaction.query.join(Category).join(Account)
    query = getSortClause(query, sort, sort_order)
    query = getFilterByCategory(query, category_type, category, subcategory)
    
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


@app.route('/transactionsFiltered/', methods=['GET'])
def transactionsFiltered():
    sort, sort_order, filter_param, page_number, per_page = getParams(request)
    if filter_param is not None:
        filter_param = json.loads(filter_param)
    query = get_transaction_query( sort=sort, sort_order=sort_order, 
            category_type=filter_param.get('type'), category=filter_param.get('category'), subcategory=filter_param.get('subcategory'),
            bankName=filter_param.get('bankName'), fromDate=filter_param.get('fromDate'), toDate=filter_param.get('toDate'), 
            fromAmount=filter_param.get('fromAmount'), toAmount=filter_param.get('toAmount'), description=filter_param.get('Description'), 
            exclude_budget=True)
    total = len(query.all())
    query = getLimitClause(query, page_number, per_page)
    output =  TransactionsSchema(many=True).dump(query.all()).data
    return getResponse('transactions', total, per_page, page_number, output)


@app.route('/transactions/', methods=['POST'])
def post_transactions():
    transaction_id = request.form.get('transaction_id')
    description = request.form.get('Description')
    transaction_number = request.form.get('TransactionNumber')
    currency = request.form.get('Currency')
    amount = request.form.get('Amount')
    bank_name = request.form.get('BankName')
    amountEUR = request.form.get('AmountEUR')
    running_balance = request.form.get('RunningBalance')
    date = request.form.get('Date')
    if request.form.get('category_id') is None:
        category_id = Category.query.filter(Category.Type == request.form.get('Type')).\
            filter(Category.Category == request.form.get('Category')).\
            filter(Category.SubCategory == request.form.get('SubCategory')).first().id
    else:
        category_id = request.form.get('category_id')
    
    transaction_id = update_insert_transaction(transaction_id=transaction_id, description=description, transaction_number=transaction_number, \
        currency=currency, amount=amount, amountEUR=amountEUR, running_balance=running_balance, date=date, payment_date=date, category_id=category_id, \
        bank_name=bank_name)
    return getResponse('insert transaction', None, None, None, transaction_id)

@app.route('/splitTransaction/', methods=['POST'])
def split_transactions():
    original_transaction_id = request.form['transaction_id']
    new_category_id = request.form['new_category_id']
    new_amount_eur =request.form['new_amount_EUR']
    print(original_transaction_id, new_category_id, new_amount_eur )

    existing = Transaction.query.filter_by(id=original_transaction_id ).first()
    existing.AmountEUR = float(existing.AmountEUR) - float(new_amount_eur)
    new = Transaction(
        Description=existing.Description, TransactionNumber=existing.TransactionNumber, Currency=existing.Currency, \
        Amount=0, AmountEUR=float(new_amount_eur), RunningBalance=float(existing.RunningBalance), Date=existing.Date, \
        category_id=new_category_id, account = existing.account, PaymentDate=existing.PaymentDate)
    try:
        db.session.add(new)
        db.session.commit()
        return getResponse('splitTransaction', None, None, None, 'sucess')
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

@app.route('/SavingsAccounts/', methods=['GET']) 
def getSavingsAccounts():
    query = Account.query.filter(Account.Active==1).filter(Account.Type=='Savings').distinct()
    return getResponse('data', None, None, None, AccountSchema(many=True).dump(query).data)

@app.route('/getFilterData/', methods=['GET'])
def filter_data():
    query = Category.query.all()
    return getResponse('data', None, None, None, CategorySchema(many=True).dump(query).data)

@app.route('/categories/', methods=['POST'])
def post_categories():
    category_description_id = request.form['id']
    category_id = request.form['selectedCategoryid']
    category_description = request.form['description']
    if category_description_id == '':
        new = Categorydescription(Description=category_description, category_id=category_id)
        db.session.add(new)
        db.session.commit()
        return getResponse('category new', None, None, None, new.id)
    else:
        to_update = Categorydescription.query.filter_by(id=category_description_id).first()
        to_update.Description = category_description
        db.session.commit()
        return getResponse('category updated', None, None, None, category_id)

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category_id(id):
    title = request.form.get("title")
    to_be_deleted = Categorydescription.query.filter_by(id=id).first()
    db.session.delete(to_be_deleted)
    db.session.commit()
    return getResponse('category deleted', None, None, None, id)

@app.route('/categories/', methods=['GET'])
def categories():
    sort, sort_order, filter_param, page_number, per_page = getParams(request)
    query = Categorydescription.query.join(Category)
    total = len(query.all())
    query = getSortClause(query, sort, sort_order)
    if filter_param is not None:
        filter_param = json.loads(filter_param)
        query = getFilterByCategory(query, filter_param.get('type'), filter_param.get('category'), filter_param.get('subcategory'))
        if filter_param.get('description'):
            query = query.filter( Categorydescription.Description.like("%"+filter_param.get('description')+"%") )
    query = getLimitClause(query, page_number, per_page)
    output =  CategorydescriptionSchema(many=True).dump(query.all()).data
    return getResponse('category', total, per_page, page_number, output)

#ESTATE
@app.route('/estate/', methods=['GET'])
def getEstate():
    subq = db.session.query(
        Transaction.BankName,
        func.max(Transaction.Date).label('maxdate')).join(Account).filter(Account.Active==1).\
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
    return getResponse('estate', None, None, None, output)

# BUDGET
@app.route('/budget/', methods=['GET'])
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
    return getResponse('Budget', None, None, 1, output)

@app.route('/budget/', methods=['POST'])
def post_budget():
    transaction_id=request.form['id']
    category_id=request.form['CategoryId']
    value=request.form['Value']
    day=request.form['Day']
    month=request.form['Month']
    year=request.form['Year']
    date = datetime(year= int(year), month= int(month), day= int(day))
    update_insert_transaction(transaction_id=transaction_id, description='Budget entry', currency='EUR', \
        amount=value, amountEUR=value, running_balance=0, date=date, payment_date=date, category_id=category_id, \
        bank_name='Budget')
    return getResponse('post budget', None, None, None, 'sucess')


#INVESTMENT
@app.route('/Investment/', methods=['GET'])
def getInvestment():
    query = db.session.query(
        Transaction.BankName,
        func.max(Transaction.id).label('max_transaction_id')
    ).group_by(Transaction.BankName).join(Account).filter(Account.Active == 1).filter(Account.Type=='Savings').\
    with_entities(Transaction.Date, Transaction.RunningBalance, Transaction.BankName)

    total = len(query.all())
    output =  TransactionsSchema(many=True).dump(query.all()).data
    return getResponse('investments', total, 100, 0, output)

# CASH_FLOW
@app.route('/cashFlow/', methods=['GET'])
def getCashFlow():
    filter_param = request.args.get('filter')
    today = datetime.today()
    beginning_of_current_month = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')

    if filter_param is not None:
        filter_param = json.loads(filter_param)
        from_date = filter_param.get("fromDate")
        to_date = filter_param.get("toDate")
    else:
        from_date = beginning_of_current_month
        to_date = datetime(today.year, 12, 31).strftime('%Y-%m-%d')

    query = Transaction.query.filter(Transaction.Date >= from_date).filter(Transaction.Date <= to_date).order_by(Transaction.Date)
    output =  TransactionsSchema(many=True).dump(query.all()).data
    return getResponse('cash_flow', None, None, 1, output)
    
@app.route('/RunningBalance/', methods=['GET'])
def getRunningBalance():
    filter_param = request.args.get('filter')
    if filter_param is not None:
        filter_param = json.loads(filter_param)
        by_date = filter_param.get("byDate")
    else:
        by_date = datetime.today().strftime('%Y-%m-%d')

    q1 = db.session.query(
        Transaction.BankName,
        func.max(Transaction.Date).label('maxdate')).join(Account).filter(Account.Active==1).filter(Account.Type!='Savings').\
        group_by(Transaction.BankName).subquery('t1')

    q2 = db.session.query(
        Transaction.BankName,
        func.max(Transaction.id).label('maxid')).\
        join(q1, and_( q1.c.BankName == Transaction.BankName, q1.c.maxdate == Transaction.Date) ).\
        group_by(Transaction.BankName).subquery('t2')

    q3 = db.session.query(
        Transaction.BankName, Transaction.id, Transaction.RunningBalance).\
        join(q2, and_( q2.c.BankName == Transaction.BankName, q2.c.maxid == Transaction.id) )

    output =  TransactionsSchema(many=True).dump(q3.all()).data
    return getResponse('RunningBalance',  None, None, 1, output)

@app.route('/processData/', methods=['GET'])
def process_data():
    folder = request.args.get('folder')
    Processor(folder).process()
    return getResponse('processData', None, None, 1, 'ok')

@app.route('/updateRunningBalance/', methods=['GET'])
def udpate_runnning_balance():
    running_balance_perBank = {}
    transactions = Transaction.query.filter().filter(Transaction.BankName != 'Budget').order_by(Transaction.Date).all()
    i=0
    num_transactions = len(transactions)
    for t in transactions:
        t.RunningBalance = running_balance_perBank.get(t.BankName, 0) + t.Amount
        update_insert_transaction(transaction_id=t.id, running_balance=t.RunningBalance)
        running_balance_perBank[t.BankName] = t.RunningBalance
        i=i+1
    return getResponse('updateRunningBalance', None, None, 1, 'ok')
