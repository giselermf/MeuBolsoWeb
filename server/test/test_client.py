import re
import unittest
import json
from server.app import create_app, db

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        for rule in self.client.application.url_map.iter_rules():
            print('*****',rule)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_database_empty(self):
        response = self.client.get('/estate/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data).get('data'), [])

if __name__ == '__main__':
    unittest.main()