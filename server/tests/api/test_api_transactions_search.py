import unittest
import json
from server.app import create_app, db
from server.app.models import Transaction, Category, Account, PendingReconciliation
import pandas as pd
from server.tests.basic_test import BasicTest
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
        self.account = self.create_accounts()

    def tearDown(self):
        super(BasicTest, self).tearDown()

    def assertTransaction(self, transaction, BankName, Currency, Amount, AmountEUR, Date, Description, TransactionNumber, RunningBalance):
        self.assertEqual(transaction.BankName, BankName)
        self.assertEqual(transaction.Currency, Currency)
        self.assertEqual(transaction.Amount, Amount)
        self.assertEqual(transaction.AmountEUR, AmountEUR)
        self.assertEqual(transaction.Date.__str__(), Date)
        self.assertEqual(transaction.Description, Description)
        self.assertEqual(transaction.TransactionNumber, TransactionNumber)
        self.assertEqual(transaction.RunningBalance, RunningBalance)

    def post_transactions(self):
        response = self.client.post(
            '/transactions/',
            data=dict(
                BankName='Bank for test1 - Checking Account',
                Currency='USD',
                Amount=100,
                AmountEUR=101,
                Date='2019-01-01',
                Description='test transaction',
                category_id=self.category.id,
                TransactionNumber='xxx'
            ))

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/transactions/',
            data=dict(
                BankName='Bank for test1 - Savings',
                Currency='USD',
                Amount=100,
                AmountEUR=101,
                Date='2019-01-01',
                Description='test transaction',
                category_id=self.category.id,
                TransactionNumber='xxx'
            ))

        self.assertEqual(response.status_code, 200)

    def test_search_filter_bank_account(self):
        self.post_transactions()
        response = self.client.get(
            '/transactionsFiltered/?sort=BankName|asc&filter={"bankNames": ["Bank for test1 - Savings"]} ')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data).get('data')
        self.assertEqual(1, len(data))
        self.assertEqual('Bank for test1 - Savings', data[0]['BankName'])

    def test_search_filter_one_account_types(self):
        self.post_transactions()
        response = self.client.get(
            '/transactionsFiltered/?sort=BankName|asc&filter={"accountTypes": ["Savings"]} ')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data).get('data')
        self.assertEqual(1, len(data))
        self.assertEqual('Bank for test1 - Savings', data[0]['BankName'])

    def test_search_filter_two_account_types(self):
        self.post_transactions()
        response = self.client.get(
            '/transactionsFiltered/?sort=BankName|asc&filter={"accountTypes": ["Savings", "Checking Account"]} ')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data).get('data')
        self.assertEqual(2, len(data))
        self.assertEqual('Bank for test1 - Savings', data[1]['BankName'])
        self.assertEqual('Bank for test1 - Checking Account',
                         data[0]['BankName'])

    def test_search_filter_two_bank_names(self):
        self.post_transactions()
        response = self.client.get(
            '/transactionsFiltered/?sort=BankName|asc&filter={"bankNames": ["Bank for test1 - Savings", "Bank for test1 - Checking Account"]} ')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data).get('data')
        self.assertEqual(2, len(data))
        self.assertEqual('Bank for test1 - Savings', data[1]['BankName'])
        self.assertEqual('Bank for test1 - Checking Account',
                         data[0]['BankName'])


if __name__ == '__main__':
    unittest.main()
