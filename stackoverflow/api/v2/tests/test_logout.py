import json
from .base_test import BaseTestCase

class TestLogout(BaseTestCase):
    def test_logout(self):
        with self.client:
            response_register = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Avril Mboya',
                    email='avril@gmail.com',
                    username='avril',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            # valid logout
            response = self.client.post(
                '/api/v2/auth/logout_access',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Access token has been revoked, you are now logged out')
            self.assertEqual(response.status_code, 200)
