import unittest
from server.process_data.entry_management import ProcessUNFCU
from server.process_data.category_management import Categories
from unittest.mock import MagicMock
from datetime import datetime

class TestUNFCU(unittest.TestCase):

    def setUp(self):
        self.mock_categories = Categories()
        self.mock_categories.get_category = MagicMock(return_value='mocked_category')

    def test_entry_with_zero_amount(self):
        input_processor = ProcessUNFCU(self.mock_categories)
        row = "UNFCU Visa Elite , 4024830900084389, 09/23/2017, 0.00, , 7267 91.00 978 1.200439560, 7267 91.00 978 1.200439560"
        entry = input_processor.process(row.split(","))
        self.assertIsNone(entry)
    
    def test_real_entry(self):
        input_processor = ProcessUNFCU(self.mock_categories)
        row = "UNFCU Visa Elite , 4024830900084389, 09/23/2017, 109.24, , 74570498B7PS3T18K BOHEMIA KRYSTAL CHVALOVICE CZ, BOHEMIA KRYSTAL CHVALOVICE CZ"
        entry = input_processor.process(row.split(","))
        self.assertIsNotNone(entry)
        self.assertEqual(entry['Description'], "74570498B7PS3T18K BOHEMIA KRYSTAL CHVALOVICE CZ BOHEMIA KRYSTAL CHVALOVICE CZ")
        self.assertEqual(entry['Number'], '74570498B7PS3T18K')
        self.assertEqual(entry['Date'], datetime(2017, 9, 23, 0, 0))
        self.assertEqual(entry['PaymentDate'], datetime(2017, 9, 23, 0, 0))
        self.assertEqual(entry['Amount'], -109.24)
        self.assertEqual(entry['Currency'], "USD")
        self.assertEqual(entry['Bank Name'], "UNFCU - UNFCU Visa Elite  4024830900084389")
        self.assertTrue(entry['Amount in EUR'] > -109.24)
        self.assertEqual(entry['category_id'], 'mocked_category')

    def test_many_rows(self):
        input_processor = ProcessUNFCU(self.mock_categories)
        row = "UNFCU Visa Elite , 4024830900084389, 09/23/2017, 0.00, , 7267 91.00 978 1.200439560, 7267 91.00 978 1.200439560"
        entry = input_processor.process(row.split(","))
        self.assertIsNone(entry)
        row = "UNFCU Visa Elite , 4024830900084389, 09/23/2017, 109.24, , 74570498B7PS3T18K BOHEMIA KRYSTAL CHVALOVICE CZ, BOHEMIA KRYSTAL CHVALOVICE CZ"
        entry = input_processor.process(row.split(","))
        self.assertEqual(entry['Amount'], -109.24)
        self.assertEqual(entry['Currency'], "USD")
        self.assertTrue(entry['Amount in EUR'] > -109.24)
        ###
        row = "UNFCU Visa Elite , 4024830900084389, 09/23/2017, 0.00, , 7267 91.00 978 1.56789, 7267 91.00 978 1.200439560"
        entry = input_processor.process(row.split(","))
        self.assertIsNone(entry)
        row = "UNFCU Visa Elite , 4024830900084389, 09/23/2017, -100, , 74570498B7PS3T18K BOHEMIA KRYSTAL CHVALOVICE CZ, BOHEMIA KRYSTAL CHVALOVICE CZ"
        entry = input_processor.process(row.split(","))
        self.assertEqual(entry['Amount'], 100)
        self.assertEqual(entry['Currency'], "USD")
        self.assertTrue(entry['Amount in EUR'] < 100)

if __name__ == '__main__':
    unittest.main()