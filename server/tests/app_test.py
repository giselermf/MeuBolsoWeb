import unittest
from server.app import update_insert_transaction

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dal.db_init('sqlite:///:memory:')

    # def test_Transaction_insert(self): 
    #     results = update_insert_transaction(transaction_id=None, description="desc", transaction_number=111,\
    #         currency="EUR", amount=10, amountEUR=10, running_balance=10, date='2019-01-01', payment_date='2019-01-01',\
    #         category_id=None, bank_name='Bank Test')
    #     self.assertEqual(results, [])