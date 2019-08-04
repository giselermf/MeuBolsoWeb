import unittest
import json
from server.app import create_app, db
from server.app.models import Transaction, Category, Account, PendingReconciliation
import pandas as pd
from .basic_test import BasicTest
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
            Account(BankName='Checking Account1', Active=True,
                    Type='Checking Account', Currency='EUR')])


        self.category = self.create_category("Expense", "Home", "TV")
        db.session.commit()

    def test_running_balance_transactions_same_day(self):
        t_date_01_2017 = pd.to_datetime('2017-01-01').date()

        db.session.add_all([
            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id,
                Amount=30, AmountEUR=30, RunningBalance=0,  PaymentDate=t_date_01_2017,
                Date=t_date_01_2017, BankName='Checking Account1'),

            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id,
                Amount=100, AmountEUR=100, RunningBalance=0,  PaymentDate=t_date_01_2017,
                Date=t_date_01_2017, BankName='Checking Account1'),

            Transaction(
                Description='d', TransactionNumber='n', Currency='EUR', category_id=self.category.id,
                Amount=20, AmountEUR=20, RunningBalance=0,  PaymentDate=t_date_01_2017,
                Date=t_date_01_2017, BankName='Checking Account1')])

        db.session.commit()

        self.assertEqual(self.client.get(
            '/updateRunningBalance/').status_code, 200)
        
        response = self.client.get('/estate/?Date=2017-01-01')
        output = json.loads(response.data).get('data')
        self.assertEqual({'BankName': 'Checking Account1',
                          'RunningBalance': 150.0, 'Date': '2017-01-01', 'Type': 'Checking Account'}, output[0])




if __name__ == '__main__':
    unittest.main()
