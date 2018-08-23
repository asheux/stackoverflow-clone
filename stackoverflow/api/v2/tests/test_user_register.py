"""
Imports

"""

import json
from .base_test import BaseTestCase

def register(client):
    """registration details"""
    response = client.post(
        '/api/v2/auth/register',
        data=json.dumps(dict(
            name='Paulla Mboya',
            email='paulla@gmail.com',
            username='paulla',
            password='Mermaid12'
        )),
        content_type='application/json'
    )
    return response


class TestUserRegister(BaseTestCase):
    """Test user register resource"""
    def test_registration(self):
        """Test user successfully registers"""
        with self.client:
            response = register(self.client)
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'user created successfully')
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(response.status_code, 201)

    def test_registration_with_invalid_email(self):
        """Test user register with invalid email"""
        with self.client:
            response = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Paulla Mboya',
                    email='paullagmail.com',
                    username='paulla',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'error')
            self.assertEqual(response.status_code, 403)

    def test_registration_if_user_exits(self):
        """Test user registers if a user exists"""
        with self.client:
            response = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Paulla Mboya',
                    email='paulla@gmail.com',
                    username='paulla',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Paulla Mboya',
                    email='paulla@gmail.com',
                    username='paulla',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )

            response_data = json.loads(response.data.decode())
            errors = {
                "username": "The username you provided already exists",
                "email": "The email you provided is in use by another user"
            }
            self.assertTrue(response_data['status'] == 'error')
            self.assertTrue(response_data['message'] == errors)
            self.assertEqual(response.status_code, 401)
