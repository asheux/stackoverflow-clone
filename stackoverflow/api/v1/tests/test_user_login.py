import json
from .base_test import BaseTestCase

class TestUserLogin(BaseTestCase):
    def test_login(self):
        with self.client:
            response_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='Stacy Mboya',
                    email='stacy@gmail.com',
                    username='stacy',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='stacy',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Successfully logged in as Stacy Mboya')
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(response.status_code, 201)

    def test_login_with_none_existing_username(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='chessi',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'The username you provided does not exist')
            self.assertEqual(response.status_code, 404)

    def test_login_with_a_wrong_password(self):
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='stacy',
                    password='chessi'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'The password you provided did not match the database password')
            self.assertEqual(response.status_code, 401)
