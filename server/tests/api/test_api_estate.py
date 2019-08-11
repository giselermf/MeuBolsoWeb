import unittest
import json
from server.app import create_app, db
from server.app.models import Transaction, Category, Account, PendingReconciliation
import pandas as pd
from server.tests.basic_test import BasicTest
from collections import namedtuple


class Test_TestApiEstate(BasicTest):

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
            Account(BankName='Budget', Active=True,
                    Type='Budget', Currency='EUR'),
            Account(BankName='Credit Card1', Active=True,
                    Type='Credit Card', Currency='EUR'),
            Account(BankName='Credit Card2', Active=False,
                    Type='Credit Card', Currency='EUR'),
            Account(BankName='Savings1', Active=True,
                    Type='Savings', Currency='EUR'),
            Account(BankName='Savings2', Active=True,
                    Type='Savings', Currency='EUR'),
            Account(BankName='Checking Account1', Active=True,
                    Type='Checking Account', Currency='EUR'),
            Account(BankName='Checking Account2', Active=True,
                    Type='Checking Account', Currency='EUR'),
            Account(BankName='Checking Account3', Active=False, Type='Checking Account', Currency='EUR')])

        self.t_date_2017 = pd.to_datetime('2017-01-01').date()
        self.t_date_2019 = pd.to_datetime('2019-01-01').date()

        self.category = self.create_category("Expense", "Home", "TV")
        db.session.commit()

    def add_transactions(self):
        amount = 100
        db.session.add_all([
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id,
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=self.t_date_2017,
                Date=self.t_date_2017, BankName='Credit Card1'),
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id,
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=self.t_date_2019,
                Date=self.t_date_2019, BankName='Credit Card1'),
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id,
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=self.t_date_2019,
                Date=self.t_date_2019, BankName='Savings2'),
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id,
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=self.t_date_2019,
                Date=self.t_date_2019, BankName='Checking Account2'),
            # deactivated
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id, \
                Amount=amount, AmountEUR=amount, RunningBalance=0,  PaymentDate=self.t_date_2019, \
                Date=self.t_date_2019, BankName='Checking Account3')])

        db.session.commit()

    def test_first_date(self):
        self.add_transactions()
        self.assertEqual(self.client.get(
            '/updateRunningBalance/').status_code, 200)

        response = self.client.get('/estate/?Date=2017-01-01')

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data).get('data')
        self.assertEqual(1, len(output))
        self.assertEqual({'BankName': 'Credit Card1',
                          'RunningBalance': 100.0, 'Date': '2017-01-01', 'Type': 'Credit Card'}, output[0])

    def test_last_date(self):
        self.add_transactions()
        self.assertEqual(self.client.get(
            '/updateRunningBalance/').status_code, 200)

        response = self.client.get('/estate/?2019-01-01')

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data).get('data')
        self.assertEqual(3, len(output))
        self.assertEqual({'BankName': 'Checking Account2',
                          'RunningBalance': 100.0, 'Date': '2019-01-01', 'Type': 'Checking Account'}, output[0])
        self.assertEqual({'BankName': 'Credit Card1',
                          'RunningBalance': 200.0, 'Date': '2019-01-01', 'Type': 'Credit Card'}, output[1])
        self.assertEqual(
            {'BankName': 'Savings2', 'RunningBalance': 100.0, 'Date': '2019-01-01', 'Type': 'Savings'}, output[2])

    def test_two_transactions_same_day(self):
        db.session.add_all([
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id,
                Amount=100, AmountEUR=100, RunningBalance=0,  PaymentDate=self.t_date_2019,
                Date=self.t_date_2019, BankName='Credit Card1'),
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id,
                Amount=-20, AmountEUR=-20, RunningBalance=0,  PaymentDate=self.t_date_2019,
                Date=self.t_date_2019, BankName='Credit Card1')])
        self.assertEqual(self.client.get(
            '/updateRunningBalance/').status_code, 200)

        # response = self.client.get(
        #     '/transactionsFiltered/?sort=BankName|asc&filter={"bankNames": ["Credit Card1"]} ')

        # self.assertEqual(response.status_code, 200)
        # output = json.loads(response.data).get('data')
        # self.assertEqual(2, len(output))
        # self.assertEqual({}, output[1])

        response = self.client.get('/estate/?2019-01-01')

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data).get('data')
        self.assertEqual(1, len(output))
        self.assertEqual({'BankName': 'Credit Card1',
                          'RunningBalance': 80.0, 'Date': '2019-01-01', 'Type': 'Credit Card'}, output[0])





if __name__ == '__main__':
    unittest.main()
