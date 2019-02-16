from server.app.models import Transaction
import unittest
import time
from datetime import datetime
from server.app import create_app, db

class TransactionModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_transaction(self):
        all_transactions = Transaction.query.all()
        # db.session.add(t)
        # db.session.commit()
        self.assertEqual(all_transactions, [])

if __name__ == '__main__':
    unittest.main()