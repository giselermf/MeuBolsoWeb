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
        Transaction.query.delete()
        self.client = self.app.test_client()

        self.category = self.create_category("Expense", "Home", "TV")
        self.category2 = self.create_category("Expense", "Home", "Cell Phone")
        self.account = Account(BankName='Budget', Active=True, Type='Budget', Currency='EUR')
        db.session.add(self.account)
        db.session.commit()

    def add_budget_transaction(self, t_date, amount, category_id):
        existing_budget = Transaction(
            Description='Budget entry', TransactionNumber='number', Currency='EUR', \
            Amount=amount, AmountEUR=amount, RunningBalance=0, \
            Date= t_date, \
            category_id=category_id, BankName = self.account.BankName, PaymentDate=t_date)
        db.session.add(existing_budget)
        db.session.commit()
        return existing_budget

    def assertTransaction(self, transaction, BankName, Currency, Amount, AmountEUR, Date, Description, TransactionNumber):
        self.assertEqual(transaction.BankName, BankName)
        self.assertEqual(transaction.Currency, Currency)
        self.assertEqual(transaction.Amount, Amount)
        self.assertEqual(transaction.AmountEUR, AmountEUR)
        self.assertEqual(transaction.Date.__str__(), Date)
        self.assertEqual(transaction.Description, Description)
        self.assertEqual(transaction.TransactionNumber, TransactionNumber)

    def test_post_update_budget_with_category_id(self):
        existing_budget = self.add_budget_transaction(
            t_date=pd.to_datetime('2019-01-01').date(), amount=100, category_id=self.category.id)
        response = self.client.post(
            '/budget/', 
            data=dict(
                id = existing_budget.id,
                Date= '2019-01-01',
                Amount=110,
                CategoryId=self.category.id,
            ))

        self.assertEqual(response.status_code, 200)
        new_id = json.loads(response.data).get('data')
        new_transaction = Transaction.query.get(new_id)
        self.assertTransaction(new_transaction, 'Budget', 'EUR', 110, 110, '2019-01-01', 'Budget entry', 'number')
        self.assertEqual(new_transaction.category, self.category)

    def test_post_delete_budget_with_category_id(self):
        existing_budget = self.add_budget_transaction(
            t_date=pd.to_datetime('2018-01-01').date(), amount=100, category_id=self.category.id)
        response = self.client.post(
            '/budget/', 
            data=dict(
                id = existing_budget.id,
                Date= '2019-01-01',
                Amount=0,
                CategoryId=self.category.id,
            ))

        self.assertEqual(response.status_code, 200)
        new_id = json.loads(response.data).get('data')
        new_transaction = Transaction.query.get(new_id)
        self.assertIsNone(new_transaction)

    def test_post_add_budget_with_category_id(self):
        response = self.client.post(
            '/budget/', 
            data=dict(
                id = '' ,
                Date= '2019-01-01',
                Amount=101,
                CategoryId=self.category.id,
            ))

        self.assertEqual(response.status_code, 200)
        new_id = json.loads(response.data).get('data')
        new_transaction = Transaction.query.get(new_id)
        self.assertTransaction(new_transaction, 'Budget', 'EUR', 101, 101, '2019-01-01', 'Budget entry', 'number')
        self.assertEqual(new_transaction.category, self.category)

    def test_copy_budget(self):
        Transaction.query.delete()
        #should not be copied because is in past months
        not_to_be_copied = self.add_budget_transaction(
            t_date=pd.to_datetime('2018-02-01').date(), amount=100, category_id=self.category.id)
        #transactions that will be copied
        existing_budget1 = self.add_budget_transaction(
            t_date=pd.to_datetime('2019-01-01').date(), amount=100, category_id=self.category.id)
        existing_budget2 = self.add_budget_transaction(
            t_date=pd.to_datetime('2019-01-01').date(), amount=100, category_id=self.category2.id)
        #transaction that will be updated
        to_be_overriten = self.add_budget_transaction(
            t_date=pd.to_datetime('2019-02-01').date(), amount=200, category_id=self.category2.id)

        response = self.client.post(
            '/copyBudget/', 
            data=dict(
                Month=2,
                Year=2019,
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Transaction.query.all()), 5)
        current_month = pd.to_datetime("2019-02-01").date()
        previous_month_t = Transaction.query.filter(Transaction.BankName == 'Budget').filter(Transaction.Date == current_month).all()
        self.assertEqual(len(previous_month_t), 2)
        for t in previous_month_t:
            self.assertTransaction(t, 'Budget', 'EUR', 100, 100, "2019-02-01", 'Budget entry', 'number')

if __name__ == '__main__':
    unittest.main()