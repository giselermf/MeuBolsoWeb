from flask import Flask
import os
from flask import Flask
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_ECHO"] = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_name = os.path.join(BASE_DIR, 'database/dbMeuBolso.db')

print('###database_name', database_name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+database_name
db = SQLAlchemy(app)


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
    AmountEUR= db.Column(db.Float)
    RunningBalance= db.Column(db.Float)
    Date= db.Column(db.Date)
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

def update_insert_transaction(transaction_id=None, description=None, transaction_number=None, 
    currency=None, amount=None, amountEUR=None, running_balance=None, date=None, payment_date=None, 
    category_id=None, bank_name=None):
    if transaction_id == '' or transaction_id == None: # ADD
        if (running_balance):
            running_balance = float(running_balance)
        new = Transaction( id = None,
                            Description = description,
                            TransactionNumber = transaction_number,
                            Currency= currency,
                            Amount= float(amount),
                            AmountEUR= float(amountEUR),
                            RunningBalance= running_balance,
                            Date= date, 
                            TransferTo= None,
                            TransferId= None,
                            PaymentDate= date,
                            category_id = category_id,
                            BankName = bank_name)
        
        db.session.add(new)
        db.session.commit()
        return new.id
    elif amountEUR != None and float(amountEUR) == 0.0: #DELETE
        to_be_deleted = Transaction.query.filter_by(id=transaction_id ).first()
        db.session.delete(to_be_deleted)
        db.session.commit()
        return None
    else: # UPDATE
        to_update = Transaction.query.filter_by(id=transaction_id ).first()
        if category_id != None: to_update.category_id = category_id
        if transaction_number != None: to_update.TransactionNumber = transaction_number
        if running_balance != None: to_update.RunningBalance = running_balance
        if amount!= None: to_update.Amount = amount
        if amountEUR != None: to_update.AmountEUR = amountEUR
        db.session.commit()
        return transaction_id

def update_running_balance(bank_name):
    running_balance = 0
    transactions = Transaction.query.filter().filter(Transaction.BankName == bank_name).order_by(Transaction.Date).all()
    for t in transactions:
        running_balance = running_balance + t.Amount
        t.RunningBalance = running_balance
    db.session.commit()

