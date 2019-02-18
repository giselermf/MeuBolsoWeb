import unittest
from server.flasky import app as prod_app

class FlaskProductionTestCase(unittest.TestCase):
    def test_pages(self):
        self.client = prod_app.test_client()
        for rule in self.client.application.url_map.iter_rules():
            print('*****',rule)
        self.assertEqual(self.client.get('/getFilterTransactionData/').status_code, 200)
        self.assertEqual(self.client.get('/transactionsFiltered/').status_code, 200)
        self.assertEqual(self.client.get('/updateRunningBalance/').status_code, 200)
        self.assertEqual(self.client.get('/estate/').status_code, 200)

if __name__ == '__main__':
    unittest.main()
