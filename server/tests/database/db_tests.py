from server.app.models import Transaction, Category, Account, PendingReconciliation
import unittest
import time
from datetime import datetime
from server.app import create_app, db
import copy

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
        self.category = Category(Type="Expense", Category="Home", SubCategory="TV")
        db.session.add(self.category)
        db.session.commit()
        all_categories = Category.query.all()
        self.assertEqual(len(all_categories), 1)

    def create_bank(self):
        self.bank = Account(BankName="Test Bank", Active = True, Currency="EUR", Type = "Checking Account")
        db.session.add(self.bank)
        db.session.commit()
        all_banks = Account.query.all()
        self.assertEqual(len(all_banks), 1)

    def test_create_transaction_just_once(self):
        t = Transaction(Description='Description', \
            Amount =  100,
            AmountEUR = 100,
            Date = datetime.now(),
            category_id = self.category.id, \
            BankName=self.bank.BankName)
        db.session.add(t)
        db.session.commit()
        self.assertEqual(len(Transaction.query.all()), 1)
        self.assertEqual(len(PendingReconciliation.query.all()), 0)

    def test_create_transaction_twice(self):
        t1 = Transaction(Description='Description', \
            Amount =  100,
            AmountEUR = 100,
            Date = datetime.now(),
            category_id = self.category.id, \
            BankName=self.bank.BankName)
        t2 = Transaction(Description='Description', \
            Amount =  100,
            AmountEUR = 100,
            Date = datetime.now(),
            category_id = self.category.id, \
            BankName=self.bank.BankName)
        db.session.add(t1)
        db.session.commit()
        db.session.add(t2)
        db.session.commit()
        self.assertEqual(len(Transaction.query.all()), 2)
        self.assertEqual(len(PendingReconciliation.query.all()), 1)


if __name__ == '__main__':
    unittest.main()