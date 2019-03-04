import unittest
import json
from server.app import create_app, db
from server.app.models import Transaction, Category, Account, PendingReconciliation
import pandas as pd
from .basic_test import BasicTest
from collections import namedtuple

class FlaskAccountTestCase(BasicTest):
    
    def setUp(self):        
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Transaction.query.delete()
        self.client = self.app.test_client()
        self.prepare_initial_data()

    def prepare_initial_data(self):
        Account.query.delete()
        db.session.commit()
        
        db.session.add_all([
            Account(BankName='Budget', Active=True, Type='Budget', Currency='EUR'),
            Account(BankName='Credit Card1', Active=True, Type='Credit Card', Currency='EUR'),
            Account(BankName='Credit Card2', Active=False, Type='Credit Card', Currency='EUR'),
            Account(BankName='Savings1', Active=True, Type='Savings', Currency='EUR'),
            Account(BankName='Savings2', Active=True, Type='Savings', Currency='EUR'),
            Account(BankName='Checking Account1', Active=True, Type='Checking Account', Currency='EUR'),
            Account(BankName='Checking Account2', Active=True, Type='Checking Account', Currency='EUR'),
            Account(BankName='Checking Account3', Active=False, Type='Checking Account', Currency='EUR')]) 

        t_date_2017=pd.to_datetime('2017-01-01').date()
        t_date_2019=pd.to_datetime('2019-01-01').date()
        amount = 100

        self.category = self.create_category("Expense", "Home", "TV")
        db.session.commit()
        
        db.session.add_all([
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id, \
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=t_date_2017, \
                Date= t_date_2017, BankName = 'Credit Card1' ), 
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id, \
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=t_date_2019, \
                Date= t_date_2019, BankName = 'Credit Card2' ), 
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id, \
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=t_date_2019, \
                Date= t_date_2019, BankName = 'Savings2' ), 
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id, \
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=t_date_2019, \
                Date= t_date_2019, BankName = 'Checking Account2' ), 
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id, \
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=t_date_2019, \
                Date= t_date_2019, BankName = 'Checking Account3' )])

        db.session.commit()

    def test_select_accounts(self):    
        response = self.client.get('/getAllAccounts/')

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data).get('data')
        self.assertEqual(5, len(output))
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Credit Card1'}, output[0])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Credit Card2'}, output[1])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Savings2'}, output[2])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Checking Account2'}, output[3])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Checking Account3'}, output[4])

    def test_select_accounts_filter_by_dates(self):    
        response = self.client.get('/getAllAccounts/?filter={"fromDate":"2019-01-01","toDate":"2019-03-31"}')
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data).get('data')
        self.assertEqual(4, len(output))
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Credit Card2'}, output[0])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Savings2'}, output[1])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Checking Account2'}, output[2])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Checking Account3'}, output[3])

    def test_select_accounts_filter_by_type(self):    
        response = self.client.get('/getAllAccounts/?filter={"type":["Savings", "Credit Card"]}')
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data).get('data')
        self.assertEqual(3, len(output))
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Credit Card1'}, output[0])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Credit Card2'}, output[1])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Savings2'}, output[2])

    def test_select_accounts_filter_by_type_and_Active(self):    
        response = self.client.get('/getAllAccounts/?filter={"type":["Savings", "Credit Card"], "active":"True"}')
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data).get('data')
        self.assertEqual(2, len(output))
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Credit Card1'}, output[0])
        self.assertEqual({'Currency': 'EUR', 'BankName': 'Savings2'}, output[1])

if __name__ == '__main__':
    unittest.main()