import re
import unittest
# from server.app import create_app, db
# from server.flasky import app
from server.engine import app as prod_app

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        # self.app = create_app('testing')
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        # db.create_all()
        self.client = prod_app.test_client()
        # for rule in self.client.application.url_map.iter_rules():
        #     print('*****',rule)

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/estate/')
        print(response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

    # def test_register_and_login(self):
    #     # register a new account
    #     response = self.client.post('/auth/register', data={
    #         'email': 'john@example.com',
    #         'username': 'john',
    #         'password': 'cat',
    #         'password2': 'cat'
    #     })
    #     self.assertEqual(response.status_code, 302)

    #     # login with the new account
    #     response = self.client.post('/auth/login', data={
    #         'email': 'john@example.com',
    #         'password': 'cat'
    #     }, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(re.search('Hello,\s+john!',
    #                               response.get_data(as_text=True)))
    #     self.assertTrue(
    #         'You have not confirmed your account yet' in response.get_data(
    #             as_text=True))

    #     # send a confirmation token
    #     user = User.query.filter_by(email='john@example.com').first()
    #     token = user.generate_confirmation_token()
    #     response = self.client.get('/auth/confirm/{}'.format(token),
    #                                follow_redirects=True)
    #     user.confirm(token)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(
    #         'You have confirmed your account' in response.get_data(
    #             as_text=True))

    #     # log out
    #     response = self.client.get('/auth/logout', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('You have been logged out' in response.get_data(
    #         as_text=True))