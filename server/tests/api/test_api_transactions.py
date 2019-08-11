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
        self.create_accounts()
        self.account = Account.query.first()

    def tearDown(self):
        super(BasicTest, self).tearDown()

    def assertTransaction(self, transaction, BankName, Currency, Amount, AmountEUR, Date, Description, TransactionNumber, RunningBalance):
        self.assertEqual(transaction.BankName, BankName)
        self.assertEqual(transaction.Currency, Currency)
        self.assertEqual(float(transaction.Amount), float(Amount))
        self.assertEqual(float(transaction.AmountEUR), float(AmountEUR))
        self.assertEqual(transaction.Date.__str__(), Date)
        self.assertEqual(transaction.Description, Description)
        self.assertEqual(transaction.TransactionNumber, TransactionNumber)
        self.assertEqual(transaction.RunningBalance, RunningBalance)

    def test_post_transaction_with_category_id(self):
        response = self.client.post(
            '/transactions/',
            data=dict(
                BankName='Bank for test',
                Currency='USD',
                Amount=100,
                AmountEUR=101,
                Date='2019-01-01',
                Description='test transaction',
                category_id=self.category.id,
                TransactionNumber='xxx'
            ))

        self.assertEqual(response.status_code, 200)
        new_id = json.loads(response.data).get('data')
        new_transaction = Transaction.query.get(new_id)
        self.assertTransaction(new_transaction, 'Bank for test', 'USD', 100,
                               87.5388453626, '2019-01-01', 'test transaction', 'xxx', 100)
        self.assertEqual(new_transaction.category, self.category)

    def test_post_transaction_with_category_details(self):
        response = self.client.post(
            '/transactions/',
            data=dict(
                BankName='Bank for test',
                Currency='EUR',
                Amount=100,
                Date='2019-01-01',
                Description='test transaction',
                TransactionNumber='xxx',
                Type="Expense",
                Category="Home",
                SubCategory="TV"
            ))

        self.assertEqual(response.status_code, 200)
        new_id = json.loads(response.data).get('data')
        new_transaction = Transaction.query.get(new_id)
        self.assertTransaction(new_transaction, 'Bank for test', 'EUR',
                               100, 100, '2019-01-01', 'test transaction', 'xxx', 100)
        self.assertEqual(new_transaction.category, self.category)

    def test_delete_transaction(self):
        # INSERT
        new = Transaction(
            Description='description', Currency='EUR',
            Amount=100, AmountEUR=100,
            Date=pd.to_datetime('2019-01-01').date(),
            category_id=self.category.id, BankName=self.account.BankName)
        db.session.add(new)
        db.session.commit()

        # DELETE
        response = self.client.post(
            '/transactions/',
            data=dict(
                transaction_id=new.id,
                Amount=0,
            ))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Transaction.query.get(new.id))

    def test_update_transaction(self):
        # INSERT
        new = Transaction(
            Description='description', Currency='USD',
            Amount=100,
            Date=pd.to_datetime('2019-01-01').date(),
            category_id=self.category.id, BankName=self.account.BankName)
        db.session.add(new)
        db.session.commit()

        new_transaction = Transaction.query.get(new.id)
        self.assertTransaction(new_transaction, self.account.BankName, 'USD',
                               100, 87.5388453626, '2019-01-01', 'description', None, None)
        self.assertEqual(new_transaction.category, self.category)

        # UPDATE
        response = self.client.post(
            '/transactions/',
            data=dict(
                transaction_id=new.id,
                Amount=200,
                Date=pd.to_datetime('2019-01-01').date(),
                category_id=self.category2.id,
                TransactionNumber='xxx'
            ))
        self.assertEqual(response.status_code, 200)
        updated_transaction = Transaction.query.get(new.id)
        self.assertTransaction(new_transaction, self.account.BankName, 'USD',
                               200, 175.0776907253, '2019-01-01', 'description', 'xxx', 200)
        self.assertEqual(new_transaction.category, self.category2)


if __name__ == '__main__':
    unittest.main()
