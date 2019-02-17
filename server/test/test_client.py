import re
import unittest
import json
from server.app import create_app, db
from server.app.models import Transaction, Category, Categorydescription#, Account, PendingReconciliation
from datetime import datetime
import pandas as pd

class FlaskTransactionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        # for rule in self.client.application.url_map.iter_rules():
        #     print('*****',rule)
        self.create_category()

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
        return all_categories[0].id

    def test_post_and_delete_CategoryDescription(self):
        #post
        response = self.client.post(
            '/categories/', 
            data=dict(
                selectedCategoryid=self.category.id,
                description='VIS school'
            ))
        self.assertEqual(response.status_code, 200)
        new_id = json.loads(response.data).get('data')
        new_cat_description = Categorydescription.query.get(new_id)
        self.assertEqual(new_cat_description.Description, 'VIS school')
        self.assertEqual(new_cat_description.category_id, self.category.id)
        self.assertEqual(new_cat_description.category, self.category)

        #delete
        response = self.client.delete('/categories/'+str(new_id))
        self.assertEqual(response.status_code, 200)

        #confirming from database
        cat_description = Categorydescription.query.get(new_id)
        self.assertIsNone(cat_description)

    # def test_post_transaction(self):
    #     response = self.client.post(
    #         '/transactions/', 
    #         data=dict(
    #             BankName='bank test',
    #             Currency='EUR',
    #             Amount=100,
    #             AmountEUR=100,
    #             Date=pd.to_datetime('2019-01-01').date(),
    #             PaymentDate=pd.to_datetime('2019-01-01').date(),
    #             Description='test transaction',
    #             category_id=self.category.id,
    #             TransactionNumber='xxx'
    #         ))

    #     self.assertEqual(response.status_code, 201)
    #     print(response.data)

if __name__ == '__main__':
    unittest.main()