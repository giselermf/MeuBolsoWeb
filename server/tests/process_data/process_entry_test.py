import unittest
from server.process_data.processor import Processor
from server.process_data.category_management import Categories
from unittest.mock import MagicMock
from datetime import datetime
from server.app.models import Transaction, PendingReconciliation
from server.app import create_app, db

class TestUNFCU(unittest.TestCase):

    def setUp(self):
        self.mock_categories = Categories()
        self.mock_categories.get_category = MagicMock(return_value='mocked_category')
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Transaction.query.delete()
        self.processor = Processor('fake folder')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _get_entry(self):
        entry = {}
        entry['Description'] = "74570498B7PS3T18K BOHEMIA KRYSTAL CHVALOVICE CZ BOHEMIA KRYSTAL CHVALOVICE CZ"
        entry['Number'] = "74570498B7PS3T18K"
        entry['Date'] = datetime(2017, 9, 23, 0, 0)
        entry['PaymentDate'] = datetime(2017, 9, 23, 0, 0)
        entry['Amount'] = -109.24
        entry['Currency'] = "USD"
        entry['Bank Name'] = "UNFCU - UNFCU Visa Elite  4024830900084389"
        entry['Amount in EUR'] = -109.24 * 1.12
        entry['category_id'] = 'mocked_category'
        return entry
    
    def test_insert_same_twice(self):
        entry1 = self._get_entry()
        id1 = self.processor._process_entry('fileName', entry1)
        self.assertEqual(len(Transaction.query.all()), 1)

        entry2 = self._get_entry()
        id2 = self.processor._process_entry('fileName', entry2)
        ## second one does not go to database
        self.assertEqual(len(Transaction.query.all()), 1)

        self.assertEqual(id1, id2)
    
    def test_insert_different_transactions(self):
        entry1 = self._get_entry()
        id1 = self.processor._process_entry('fileName', entry1)
        self.assertEqual(len(Transaction.query.all()), 1)

        entry2 = self._get_entry()
        entry2['Amount'] = -100
        id2 = self.processor._process_entry('fileName', entry2)
        ## second one gets recorded
        self.assertEqual(len(Transaction.query.all()), 2)
    
    def test_insert_first_does_not_have_number(self):
        entry1 = self._get_entry()
        entry1['Number'] = None
        id1 = self.processor._process_entry('fileName', entry1)
        self.assertEqual(len(Transaction.query.all()), 1)

        entry2 = self._get_entry()
        id2 = self.processor._process_entry('fileName', entry2)
        self.assertEqual(len(Transaction.query.all()), 2)
        self.assertEqual(len(PendingReconciliation.query.all()), 0)
    
    def test_insert_second_does_not_have_number(self):
        entry1 = self._get_entry()
        id1 = self.processor._process_entry('fileName', entry1)
        self.assertEqual(len(Transaction.query.all()), 1)

        entry2 = self._get_entry()
        entry2['Number'] = None
        id2 = self.processor._process_entry('fileName', entry2)
        ## second one does not go to database
        self.assertEqual(len(Transaction.query.all()), 1)

        self.assertEqual(id1, id2)

if __name__ == '__main__':
    unittest.main()