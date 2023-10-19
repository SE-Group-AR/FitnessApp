import unittest
import os,sys,inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)
from application import app
import json
from bs4 import BeautifulSoup
from flask import session

class TestApplication(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Expect a redirect status code

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)  # Expect a success status code

    def test_register_route(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)  # Expect a success status code

    def test_calories_route(self):
        # Assuming the user is logged in (session is set)
        response = self.app.get('/calories')
        self.assertEqual(response.status_code, 302)  # Expect a success status code

    # def test_display_profile_route(self):
    #     # Assuming the user is logged in (session is set)
    #     with self.app as client:
    #         with client.session_transaction() as sess:
    #             sess['email'] = 'testuser@example.com'
    #         response = client.get('/display_profile')
    #         self.assertEqual(response.status_code, 200)  # Expect a success status code

    def test_user_profile_route(self):
        # Assuming the user is logged in (session is set)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['email'] = 'testuser@example.com'
            response = client.get('/user_profile')
            self.assertEqual(response.status_code, 200)  # Expect a success status code

    def test_history_route(self):
        # Assuming the user is logged in (session is set)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['email'] = 'testuser@example.com'
            response = client.get('/history')
    
            self.assertEqual(response.status_code, 200)  # Expect a success status code
    def test_bmi_calci_post(self):
        response = self.app.post('/bmi_calc', data={'weight': 70, 'height': 175})
        self.assertEqual(response.status_code, 200)

    def test_ajaxsendrequest_route(self):
    
        with self.app as client:
            with client.session_transaction() as sess:
                sess['email'] = 'testuser@example.com'
            response = client.post('/ajaxsendrequest', data={'receiver': 'friend@example.com'})
            self.assertEqual(response.status_code, 200)  

    def test_ajaxcancelrequest_route(self):
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['email'] = 'testuser@example.com'
            response = client.post('/ajaxcancelrequest', data={'receiver': 'friend@example.com'})
            self.assertEqual(response.status_code, 200)  

    def test_ajaxapproverequest_route(self):
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['email'] = 'testuser@example.com'
            response = client.post('/ajaxapproverequest', data={'receiver': 'friend@example.com'})
            self.assertEqual(response.status_code, 200) 
   
    def test_dashboard_route(self):
    # Assuming the user is logged in (session is set)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['email'] = 'testuser@example.com'
            response = client.get('/dashboard')
            self.assertEqual(response.status_code, 200)  # Expect a success status code

    def test_add_favorite_route(self):
        # Assuming the user is logged in (session is set)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['email'] = 'testuser@example.com'
            response = client.post('/add_favorite', json={'exercise_id': '123', 'action': 'add'})
            self.assertEqual(response.status_code, 200)  # Expect a success status code

    def test_favorites_route(self):
        # Assuming the user is logged in (session is set)
        with self.app as client:
            with client.session_transaction() as sess:
                sess['email'] = 'testuser@example.com'
            response = client.get('/favorites')
            self.assertEqual(response.status_code, 200)  # Expect a success status code
if __name__ == '__main__':
    unittest.main()
