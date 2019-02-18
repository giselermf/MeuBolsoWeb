import unittest
import json
from server.app import create_app, db
from server.app.models import Category, Categorydescription
from .basic_test import BasicTest

class FlaskTransactionTestCase(BasicTest):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.clean_up_database()

        self.category = self.create_category("Expense", "Home", "TV")

    def tearDown(self):
        super(BasicTest, self).tearDown()
        
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


if __name__ == '__main__':
    unittest.main()