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

        self.categories = []
        self.categories.append(self.create_category("Expense", "Home", "TV"))
        self.categories.append(self.create_category("Expense", "Home", "Cellphone"))
        self.categories.append(self.create_category("Expense", "Kids", "School"))
        self.categories.append(self.create_category("Expense", "Kids", "Transport"))
        self.categories.append(self.create_category("Income", "Lucas", "UN"))

        self.create_category_description(self.categories[0].id, "Netflix")
        self.create_category_description(self.categories[0].id, "Sling")
        self.create_category_description(self.categories[1].id, "Drei")
        self.create_category_description(self.categories[2].id, "VIS")
        self.create_category_description(self.categories[4].id, "UN salary")


    def tearDown(self):
        super(BasicTest, self).tearDown()

    def test_get_categories_no_filter(self):
        response = self.client.get(
            '/categories/?sort=Category%7Casc&page=1&per_page=2', 
            data=dict(
            ))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result.get('per_page'), 2)
        self.assertEqual(result.get('current_page'), 1)
        self.assertEqual(result.get('last_page'), 3)
        self.assertEqual(result.get('total'), 5)
        self.assertEqual(result.get('next_page_url'), 'category?page=2')
        self.assertEqual(result.get('prev_page_url'), 'category?page=0')
        self.assertEqual(result.get('from'), 1)
        self.assertEqual(result.get('to'), 3)
        self.assertEqual(len(result.get('data')), 2)
        self.assertEqual(result.get('data')[0].get('Description'), 'Netflix' )
        self.assertEqual(result.get('data')[0].get('category').get('Category'), 'Home' )
        self.assertEqual(result.get('data')[0].get('category').get('Type'), 'Expense' )
        self.assertEqual(result.get('data')[0].get('category').get('SubCategory'), 'TV' )
        self.assertEqual(result.get('data')[0].get('category').get('id'), 1 )
        
    def test_get_categories_with_type_filter(self):
        response = self.client.get(
            'categories/?filter=%7B"type":"Expense"%7D') 
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(len(result.get('data')), 4)
        all_descriptions_for_expenses = list(map(lambda x: x.get('Description'), result.get('data')))
        self.assertListEqual(all_descriptions_for_expenses, ['Netflix', 'Sling', 'Drei', 'VIS'])
    
    def test_get_categories_with_type_filter2(self):
        response = self.client.get(
            'categories/?filter=%7B"type":"Income"%7D') 
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(len(result.get('data')), 1)
        all_descriptions_for_expenses = list(map(lambda x: x.get('Description'), result.get('data')))
        self.assertListEqual(all_descriptions_for_expenses, ["UN salary"])

    def test_get_categories_with_type_filter_no_results(self):
        response = self.client.get(
            'categories/?sort=Category&filter=%7B"type":"dont exist"%7D') 
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(len(result.get('data')), 0)
        all_descriptions_for_expenses = list(map(lambda x: x.get('Description'), result.get('data')))
        self.assertListEqual(all_descriptions_for_expenses, [])

    def test_get_categories_with_description_filter(self):
        response = self.client.get(
            'categories/?filter=%7B"description":"salar"%7D') 
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(len(result.get('data')), 1)
        all_descriptions_for_expenses = list(map(lambda x: x.get('Description'), result.get('data')))
        self.assertListEqual(all_descriptions_for_expenses, ["UN salary"])

# #category: this.$refs.typecombos.getSelectedCategory(),
#         subcategory: this.$refs.typecombos.getSelectedSubCategory(),
#         description: this.description,
#         type: this.$refs.typecombos.getSelectedType()

    def test_post_and_delete_CategoryDescription(self):
        #post
        response = self.client.post(
            '/categories/', 
            data=dict(
                selectedCategoryid=self.categories[0].id,
                description='VIS school'
            ))
        self.assertEqual(response.status_code, 200)
        new_id = json.loads(response.data).get('data')
        new_cat_description = Categorydescription.query.get(new_id)
        self.assertEqual(new_cat_description.Description, 'VIS school')
        self.assertEqual(new_cat_description.category_id, self.categories[0].id)
        self.assertEqual(new_cat_description.category, self.categories[0])

        #delete
        response = self.client.delete('/categories/'+str(new_id))
        self.assertEqual(response.status_code, 200)

        #confirming from database
        cat_description = Categorydescription.query.get(new_id)
        self.assertIsNone(cat_description)


if __name__ == '__main__':
    unittest.main()