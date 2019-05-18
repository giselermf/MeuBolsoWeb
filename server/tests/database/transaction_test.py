from server.app.models import Transaction, Category, Account, PendingReconciliation, TransactionsSchema
import unittest
import time
from datetime import datetime
from server.app import create_app, db
import copy
from server.app.main.engine import get_transaction_query
import json


class TransactionModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.create_category()
        self.create_bank()
        all_transactions = Transaction.query.all()
        self.assertEqual(all_transactions, [])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_category(self):
        self.category = Category(
            Type="Expense", Category="Home", SubCategory="TV")
        db.session.add(self.category)
        db.session.commit()
        all_categories = Category.query.all()
        self.assertEqual(len(all_categories), 1)

    def create_bank(self):
        self.bank = Account(BankName="Test Bank", Active=True,
                            Currency="EUR", Type="Checking Account")
        db.session.add(self.bank)
        self.bank2 = Account(BankName="Test Bank2", Active=True,
                    Currency="EUR", Type="Checking Account")
        db.session.add(self.bank2)
        db.session.commit()
        all_banks = Account.query.all()
        self.assertEqual(len(all_banks), 2)

    def test_create_transaction_just_once(self):
        t = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime.now(),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t)
        db.session.commit()
        self.assertEqual(len(Transaction.query.all()), 1)
        self.assertEqual(len(PendingReconciliation.query.all()), 0)

    def test_create_transaction_twice_with_pending_reconciliation(self):
        t1 = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime.now(),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t1)
        db.session.commit()

        t2 = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime.now(),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t2)
        db.session.commit()
        self.assertEqual(len(Transaction.query.all()), 2)
        self.assertEqual(len(PendingReconciliation.query.all()), 1)

    def test_identify_pending_reconciliation_when_date_is_not_same_but_in_range(self):
        t1 = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 15),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t1)
        db.session.commit()

        t2 = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 10),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t2)
        db.session.commit()

        self.assertEqual(len(Transaction.query.all()), 2)
        self.assertEqual(len(PendingReconciliation.query.all()), 1)

    def test_identify_pending_reconciliation_when_date_is_not_same_but_in_range2(self):
        t1 = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 15),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t1)
        db.session.commit()

        t2 = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 20),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t2)
        db.session.commit()
        self.assertEqual(len(Transaction.query.all()), 2)
        self.assertEqual(len(PendingReconciliation.query.all()), 1)

    def test_identify_pending_reconciliation_when_date_is_not_same_but_out_of_range(self):
        t1 = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 15),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t1)
        db.session.commit()

        t2 = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 5),
            category_id=self.category.id,
            BankName=self.bank.BankName)

        db.session.add(t2)
        db.session.commit()
        self.assertEqual(len(Transaction.query.all()), 2)
        self.assertEqual(len(PendingReconciliation.query.all()), 0)

    def test_identify_pending_reconciliation_when_description_is_similar(self):
        t1 = Transaction(Description='Description complete for one transaction',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 15),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t1)
        db.session.commit()

        t2 = Transaction(Description='Description',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 10),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t2)
        db.session.commit()
        self.assertEqual(len(Transaction.query.all()), 2)
        self.assertEqual(len(PendingReconciliation.query.all()), 1)

    def test_get_transaction_multiple_bank_accounts(self):
        t1 = Transaction(Description='Description for t1',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 15),
            category_id=self.category.id,
            BankName=self.bank.BankName)
        db.session.add(t1)

        t2 = Transaction(Description='Description for t2',
            Amount=100,
            Currency="EUR",
            Date=datetime(2019, 1, 15),
            category_id=self.category.id,
            BankName=self.bank2.BankName)
        db.session.add(t2)

        db.session.commit()

        query = get_transaction_query("Date", "desc", bankNames=["Test Bank"])
        output =  TransactionsSchema(many=True).dump(query.all()).data
        self.assertEqual(output[0]['Description'], "Description for t1")
        self.assertEqual(output[0]['BankName'], "Test Bank")
   
        query = get_transaction_query("Date", "desc", bankNames=["Test Bank2"])
        output =  TransactionsSchema(many=True).dump(query.all()).data
        self.assertEqual(output[0]['Description'], "Description for t2")
        self.assertEqual(output[0]['BankName'], "Test Bank2")


if __name__ == '__main__':
    unittest.main()
