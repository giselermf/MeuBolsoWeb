from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.orm import object_session
from marshmallow import Schema
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.fields import Int, String, Float, Nested
from server.app import db
# from server.flasky import ma

class Account(db.Model):
    BankName = db.Column(db.String(30), primary_key=True)
    Active = db.Column(db.Boolean)
    Type = db.Column(db.String(15))
    Currency= db.Column(db.String(6))

class Categorydescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(50), nullable=False)
    Category = db.Column(db.String(50), nullable=False)
    SubCategory = db.Column(db.String(50), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(100), nullable=False)
    TransactionNumber = db.Column(db.String(10))
    Currency= db.Column(db.String(6))
    Amount= db.Column(db.Float)
    AmountEUR= db.Column(db.Float, nullable=False)
    RunningBalance= db.Column(db.Float)
    Date= db.Column(db.Date, nullable=False)
    TransferTo= db.Column(db.String(100))
    TransferId= db.Column(db.Integer)
    PaymentDate= db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category')
    BankName= db.Column(db.String(100), db.ForeignKey('account.BankName'), nullable=False)
    account = db.relationship('Account')

    @hybrid_property
    def Day(self):
        return self.Date.day

    @hybrid_property
    def Month(self):
        return self.Date.month

    @hybrid_property
    def Year(self):
        return self.Date.year
    
    @hybrid_property
    def Category(self):
        return self.category.Category

    @hybrid_property
    def Type(self):
        return self.category.Type

    @hybrid_property
    def SubCategory(self):
        return self.category.SubCategory
    
    @hybrid_property
    def Active(self):
        return self.account.Active

    def update(self, category_id, transaction_number, running_balance, amount, amountEUR):
        if category_id != None: self.category_id = category_id
        if transaction_number != None: self.TransactionNumber = transaction_number
        if running_balance != None: self.RunningBalance = running_balance
        if amount!= None: self.Amount = amount
        if amountEUR != None: self.AmountEUR = amountEUR
        

# standard decorator style
@event.listens_for(Transaction, 'after_insert')
def receive_after_insert(mapper, connection, target):
    transactions_in_db = get_similar_transaction(target.TransactionNumber, target.Currency, target.BankName, target.Amount, target.Date, target.Description)
    if len(transactions_in_db) > 1: # has similars, not only the recent entry
        for t in transactions_in_db:
            if t.id != target.id:
                object_session(target).add(PendingReconciliation(transaction_id1 = t.id, transaction_id2 = target.id ))


class PendingReconciliation(db.Model):
    __tablename__ = 'PendingReconciliation'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id1 = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    transaction_id2 = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    transaction1 = db.relationship('Transaction', foreign_keys=[transaction_id1])
    transaction2 = db.relationship('Transaction', foreign_keys=[transaction_id2])


class CategorySchema(ModelSchema):
    class Meta:
        model = Category

class CategorydescriptionSchema(ModelSchema):
    class Meta:
        model = Categorydescription
    category = Nested(CategorySchema)

class AccountSchema(ModelSchema):
    class Meta:
        model = Account     

class TransactionsSchema(ModelSchema):
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

class PendingReconciliationSchema(ModelSchema):
    class Meta:
        model = PendingReconciliation
    transaction1 = Nested(TransactionsSchema)
    transaction2 = Nested(TransactionsSchema)

class BudgetSchema(ModelSchema):
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

class TransactionsFilterSchema(Schema):
    class Meta:
        fields = ('BankName', 'Type', 'Category', 'SubCategory')


def get_similar_transaction(transaction_number, currency, bankName, amount, date, description):
    return Transaction.query.\
            filter(Transaction.TransactionNumber == transaction_number).\
            filter(Transaction.Currency == currency).\
            filter(Transaction.BankName == bankName).\
            filter(Transaction.Amount == amount).\
            filter(Transaction.Date == date.strftime ('%Y-%m-%d') ).\
            filter(Transaction.Description.like("%"+description[:30]+"%")).all()

def update_running_balance(bank_name):
    running_balance = 0
    transactions = Transaction.query.filter().filter(Transaction.BankName == bank_name).order_by(Transaction.Date).all()
    for t in transactions:
        running_balance = running_balance + t.Amount
        t.RunningBalance = running_balance
    db.session.commit()
