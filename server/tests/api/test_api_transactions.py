import unittest
import json
from server.app import create_app, db
from server.app.models import Transaction, Category, Account, PendingReconciliation
import pandas as pd
from .basic_test import BasicTest
from collections import namedtuple

class FlaskTransactionTestCase(BasicTest):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        self.clean_up_database()

        self.category = self.create_category("Expense", "Home", "TV")
        self.category2 = self.create_category("Expense", "Home", "Cell Phone")
        self.account = self.create_account()

    def tearDown(self):
        super(BasicTest, self).tearDown()

    def assertTransaction(self, transaction, BankName, Currency, Amount, AmountEUR, Date, Description, TransactionNumber):
        self.assertEqual(transaction.BankName, BankName)
        self.assertEqual(transaction.Currency, Currency)
        self.assertEqual(transaction.Amount, Amount)
        self.assertEqual(transaction.AmountEUR, AmountEUR)
        self.assertEqual(transaction.Date.__str__(), Date)
        self.assertEqual(transaction.Description, Description)
        self.assertEqual(transaction.TransactionNumber, TransactionNumber)

    def test_post_transaction_with_category_id(self):
        response = self.client.post(
            '/transactions/', 
            data=dict(
                BankName='Bank for test',
                Currency='EUR',
                Amount=100,
                AmountEUR=101,
                Date= '2019-01-01',
                Description='test transaction',
                category_id=self.category.id,
                TransactionNumber='xxx'
            ))

        self.assertEqual(response.status_code, 200)
        new_id = json.loads(response.data).get('data')
        new_transaction = Transaction.query.get(new_id)
        self.assertTransaction(new_transaction, 'Bank for test', 'EUR', 100, 101, '2019-01-01', 'test transaction', 'xxx')
        self.assertEqual(new_transaction.category, self.category)

    def test_post_transaction_with_category_details(self):
        response = self.client.post(
            '/transactions/', 
            data=dict(
                BankName='Bank for test',
                Currency='EUR',
                Amount=100,
                AmountEUR=101,
                Date= '2019-01-01',
                Description='test transaction',
                TransactionNumber='xxx',
                Type="Expense", 
                Category="Home",
                SubCategory="TV"
            ))

        self.assertEqual(response.status_code, 200)
        new_id = json.loads(response.data).get('data')
        new_transaction = Transaction.query.get(new_id)
        self.assertTransaction(new_transaction, 'Bank for test', 'EUR', 100, 101, '2019-01-01', 'test transaction', 'xxx')
        self.assertEqual(new_transaction.category, self.category)

    def test_delete_transaction(self):
        #INSERT
        new = Transaction(
            Description='description', Currency='EUR', \
            Amount=100, AmountEUR=100, 
            Date=pd.to_datetime('2019-01-01').date(), \
            category_id=self.category.id, BankName = self.account.BankName)
        db.session.add(new)
        db.session.commit()
        
        #DELETE
        response = self.client.post(
            '/transactions/', 
            data=dict(
                transaction_id=new.id,
                Amount=0,
            ))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Transaction.query.get(new.id))

    def test_update_transaction(self):
        #INSERT
        new = Transaction(
            Description='description', Currency='EUR', \
            Amount=100, AmountEUR=101, 
            Date=pd.to_datetime('2019-01-01').date(), \
            category_id=self.category.id, BankName = self.account.BankName)
        db.session.add(new)
        db.session.commit()

        new_transaction = Transaction.query.get(new.id)
        self.assertTransaction(new_transaction, self.account.BankName, 'EUR', 100, 101, '2019-01-01', 'description', None)
        self.assertEqual(new_transaction.category, self.category)

        
        #UPDATE
        response = self.client.post(
            '/transactions/', 
            data=dict(
                transaction_id=new.id,
                Amount=200,
                AmountEUR=201,
                RunningBalance=2000,
                category_id=self.category2.id,
                TransactionNumber='xxx'
            ))
        self.assertEqual(response.status_code, 200)
        updated_transaction = Transaction.query.get(new.id)
        self.assertTransaction(new_transaction, self.account.BankName, 'EUR', 200, 201, '2019-01-01', 'description', 'xxx')
        self.assertEqual(new_transaction.category, self.category2)


    def test_add_future_transactions_monthly(self):
        response = self.client.post(
            '/addFutureTransactions/', 
            data=dict(
                BankName=self.account.BankName,
                Currency='EUR',
                AmountEUR=100,
                fromDate= '2019-01-01',
                frequency= "Monthly",
                numberOccurrencies= 5,
                Description='desc',
                category_id=self.category.id
            ))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data).get('data')
        results_obj = list(map(lambda d: namedtuple("t", d.keys())(*d.values()), results))
        self.assertEqual(len(results), 5)
        self.assertTransaction(results_obj[0], self.account.BankName, 'EUR', 100, 100, '2019-01-01', 'desc', 'Future')
        self.assertTransaction(results_obj[1], self.account.BankName, 'EUR', 100, 100, '2019-02-01', 'desc', 'Future')
        self.assertTransaction(results_obj[2], self.account.BankName, 'EUR', 100, 100, '2019-03-01', 'desc', 'Future')
        self.assertTransaction(results_obj[3], self.account.BankName, 'EUR', 100, 100, '2019-04-01', 'desc', 'Future')
        self.assertTransaction(results_obj[4], self.account.BankName, 'EUR', 100, 100, '2019-05-01', 'desc', 'Future')

    def test_add_future_transactions_quartely(self):
        response = self.client.post(
            '/addFutureTransactions/', 
            data=dict(
                BankName=self.account.BankName,
                Currency='EUR',
                AmountEUR=100,
                fromDate= '2019-01-01',
                frequency= "Quartely",
                numberOccurrencies= 3,
                Description='desc',
                category_id=self.category.id
            ))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data).get('data')
        results_obj = list(map(lambda d: namedtuple("t", d.keys())(*d.values()), results))
        self.assertEqual(len(results), 3)
        self.assertTransaction(results_obj[0], self.account.BankName, 'EUR', 100, 100, '2019-01-01', 'desc', 'Future')
        self.assertTransaction(results_obj[1], self.account.BankName, 'EUR', 100, 100, '2019-04-01', 'desc', 'Future')
        self.assertTransaction(results_obj[2], self.account.BankName, 'EUR', 100, 100, '2019-07-01', 'desc', 'Future')

    def test_add_future_transactions_yearly(self):
        response = self.client.post(
            '/addFutureTransactions/', 
            data=dict(
                BankName=self.account.BankName,
                Currency='EUR',
                AmountEUR=100,
                fromDate= '2019-01-01',
                frequency= "Yearly",
                numberOccurrencies= 3,
                Description='desc',
                category_id=self.category.id
            ))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data).get('data')
        results_obj = list(map(lambda d: namedtuple("t", d.keys())(*d.values()), results))
        self.assertEqual(len(results), 3)
        self.assertTransaction(results_obj[0], self.account.BankName, 'EUR', 100, 100, '2019-01-01', 'desc', 'Future')
        self.assertTransaction(results_obj[1], self.account.BankName, 'EUR', 100, 100, '2020-01-01', 'desc', 'Future')
        self.assertTransaction(results_obj[2], self.account.BankName, 'EUR', 100, 100, '2021-01-01', 'desc', 'Future')
    
    def test_add_future_transactions_weekly(self):
        response = self.client.post(
            '/addFutureTransactions/', 
            data=dict(
                BankName=self.account.BankName,
                Currency='EUR',
                AmountEUR=100,
                fromDate= '2019-01-01',
                frequency= "Weekly",
                numberOccurrencies= 3,
                Description='desc',
                category_id=self.category.id
            ))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data).get('data')
        results_obj = list(map(lambda d: namedtuple("t", d.keys())(*d.values()), results))
        self.assertEqual(len(results), 3)
        self.assertTransaction(results_obj[0], self.account.BankName, 'EUR', 100, 100, '2019-01-01', 'desc', 'Future')
        self.assertTransaction(results_obj[1], self.account.BankName, 'EUR', 100, 100, '2019-01-08', 'desc', 'Future')
        self.assertTransaction(results_obj[2], self.account.BankName, 'EUR', 100, 100, '2019-01-15', 'desc', 'Future')
    


if __name__ == '__main__':
    unittest.main()