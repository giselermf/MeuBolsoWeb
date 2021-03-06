import unittest
from server.app import db
from server.app.models import Category, Account, Categorydescription, Transaction

class BasicTest(unittest.TestCase):
    def clean_up_database(self):
        Category.query.delete()
        Transaction.query.delete()
        Account.query.delete()
        Categorydescription.query.delete()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_category(self, typec, category, subCategory):
        new = Category(Type=typec, Category=category, SubCategory=subCategory)
        db.session.add(new)
        db.session.commit()
        return new

    def create_category_description(self, category_id, description):
        new = Categorydescription(category_id=category_id, Description=description)
        db.session.add(new)
        db.session.commit()
        return new

    def create_accounts(self):
        db.session.add(Account(BankName='Bank for test1 - Checking Account', Active=True, Type='Checking Account', Currency='EUR'))
        db.session.add(Account(BankName='Bank for test2 - Checking Account', Active=True, Type='Checking Account', Currency='EUR'))
        db.session.add(Account(BankName='Bank for test1 - Savings', Active=True, Type='Savings', Currency='EUR'))
        db.session.add(Account(BankName='Bank for test2 - Savings', Active=True, Type='Savings', Currency='EUR'))

        db.session.commit()
