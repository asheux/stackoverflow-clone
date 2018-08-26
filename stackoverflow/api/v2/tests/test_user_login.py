"""
Imports

"""

import json
from .base_test import BaseTestCase

class TestUserLogin(BaseTestCase):
    """Testing user authentication"""
    def test_login(self):
        """Login tests"""
        with self.client:
            response_register = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Stacy Mboya',
                    email='stacy@gmail.com',
                    username='stacy',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v2/auth/login',
                data=json.dumps(dict(
                    username='stacy',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)

    def test_login_with_none_existing_username(self):
        """Test login with details of user that doesnt exist"""
        with self.client:
            response = self.client.post(
                '/api/v2/auth/login',
                data=json.dumps(dict(
                    username='chessi',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    def test_login_with_a_wrong_password(self):
        """Test login with wrong password"""
        with self.client:
            response_register = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Stacy Mboya',
                    email='stacy@gmail.com',
                    username='stacy',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v2/auth/login',
                data=json.dumps(dict(
                    username='stacy',
                    password='chessi'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
