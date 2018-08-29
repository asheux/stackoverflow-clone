"""
Imports

"""

import json
from .base_test import BaseTestCase

class TestUserQuestions(BaseTestCase):
    """Test user post questions"""
    def test_post_question(self):
        """Test user can post a question"""
        with self.client:
            resp_register = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Brian Mboya',
                    email='asheuh@gmail.com',
                    username='asheuh',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['access_token']
                ),
                data=json.dumps(dict(
                    title='Gjango cli',
                    description='How to create cli project in django?'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

    def test_user_retrieves_all_questions(self):
        """Test user can retrieve all questions"""
        with self.client:
            resp_register = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Brian Mboya',
                    email='asheuh@gmail.com',
                    username='asheuh',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['access_token']
                ),
                data=json.dumps(dict(
                    title='Gjango cli',
                    description='How to create cli project in django?'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 200)

    def test_user_retrieves_one_question(self):
        """Test user can retrieve one question"""
        with self.client:
            resp_register = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Brian Mboya',
                    email='asheuh@gmail.com',
                    username='asheuh',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['access_token']
                ),
                data=json.dumps(dict(
                    title='Gjango cli',
                    description='How to create cli project in django?'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 200)

    def test_user_can_delete_their_question(self):
        """Test user can delete a question"""
        with self.client:
            resp_register = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Ivy Mboya',
                    email='ivy@gmail.com',
                    username='ivy',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['access_token']
                ),
                data=json.dumps(dict(
                    title='Flask Cli',
                    description='How to create cli project in flask?'
                )),
                content_type='application/json'
            )
            resp = self.client.delete(
                '/api/v2/questions/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 200)

    def test_user_retrieves_all_their_questions(self):
        """Test user can retrieve all their questions"""
        with self.client:
            resp_register = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Brian Mboya',
                    email='asheuh@gmail.com',
                    username='asheuh',
                    password='Mermaid12'
                )),
                content_type='application/json'
            )
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['access_token']
                ),
                data=json.dumps(dict(
                    title='Gjango cli',
                    description='How to create cli project in django?'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions/myquestions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 200)
