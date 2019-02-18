import unittest
from server.app import db
from server.app.models import Category, Account

class BasicTest(unittest.TestCase):
    def clean_up_database(self):
        Category.query.delete()
        Account.query.delete()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_category(self, typec, category, subCategory):
        new = Category(Type=typec, Category=category, SubCategory=subCategory)
        db.session.add(new)
        db.session.commit()
        return new

    def create_account(self):
        new = Account(BankName='Bank for test', Active=True, Type='Checking Account', Currency='EUR')
        db.session.add(new)
        db.session.commit()
        return new