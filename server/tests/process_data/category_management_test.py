import unittest
from server.process_data.category_management import Categories
from server.tests.basic_test import BasicTest
from server.app import create_app, db
from server.app.models import Category

class TestCategoryManagement(BasicTest):

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
        self.categories.append(self.create_category("Others", "Others", "Others"))

        self.create_category_description(self.categories[0].id, "Netflix")
        self.create_category_description(self.categories[0].id, "Sling")
        self.create_category_description(self.categories[1].id, "Drei")
        self.create_category_description(self.categories[2].id, "VIS")
        self.create_category_description(self.categories[4].id, "UN salary")
        self.create_category_description(self.categories[3].id, "UN salary transport")
        self.create_category_description(self.categories[5].id, "Others")

        self.categoryManagement= Categories()

    def test_category_found(self):
        self.assertEqual(self.categories[0].id, self.categoryManagement.get_category('NetFlix bla bla bla'))
        self.assertEqual(self.categories[0].id, self.categoryManagement.get_category('bla bla Sling bla'))
        self.assertEqual(self.categories[1].id, self.categoryManagement.get_category('Drei'))
        self.assertEqual(self.categories[4].id, self.categoryManagement.get_category('UN salary'))
        self.assertEqual(self.categories[3].id, self.categoryManagement.get_category('UN salary transport'))

    def test_category_not_found(self):
        self.assertEqual(self.categories[5].id, self.categoryManagement.get_category('bla'))