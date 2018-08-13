import json
from .base_test import BaseTestCase

class TestUser(BaseTestCase):
    def test_user_can_get_their_details(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='Diana Mboya',
                    email='dee@gmail.com',
                    username='dee',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.get(
               '/api/v1/users/current',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'dee@gmail.com')
            self.assertEqual(response.status_code, 200)

    def test_user_retrieves_all_users(self):
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='dee',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v1/users',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(resp.status_code, 200)

