"""
Imports

"""

import json
from .base_test import BaseTestCase

def register(my_client):
    """Function that holds data for register"""
    resp_register = my_client.post(
        '/api/v2/auth/register',
        data=json.dumps(dict(
            name='Ivy Mboya',
            email='ivy@gmail.com',
            username='ivy',
            password='Mermaid12'
        )),
        content_type='application/json'
    )
    return resp_register

class TestAnswerAction(BaseTestCase):
    """Test answer action resource"""
    def test_user_retrieves_all_answers_to_a_questions(self):
        """Test user can retrieve all answers to a question"""
        with self.client:
            resp_register = register(self.client)
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    title='Flask Cli',
                    description='How to create cli project in flask?'
                )),
                content_type='application/json'
            )
            resp = self.client.post(
                '/api/v2/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    answer='Use click cli'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(resp.status_code, 200)

    def test_user_retrieves_all_answers_to_a_questions_if_none(self):
        """Test user cannot retrieve none answers"""
        with self.client:
            resp_register = register(self.client)
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    title='Flask Cli',
                    description='How to create cli project in flask?'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertEqual(resp.status_code, 404)

    def test_user_retrieves_all_questions_with_most_answers(self):
        """Test user can retrieve questions with most answers"""
        with self.client:
            resp_register = register(self.client)
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    title='Flask Cli',
                    description='How to create cli project in flask?'
                )),
                content_type='application/json'
            )
            resp = self.client.post(
                '/api/v2/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    answer='Use click cli'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions/mostanswers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(resp.status_code, 200)

    def test_user_retrieves_all_questions_with_most_answers_if_none(self):
        """Test user cannot retrieve questions with most answers if none"""
        with self.client:
            resp_register = register(self.client)
            resp = self.client.get(
                '/api/v2/questions/mostanswers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'There are no questions')
            self.assertEqual(resp.status_code, 404)

    def test_user_retrieves_user_search_results_of_questions(self):
        """Test user can search for an answer"""
        with self.client:
            resp_register = register(self.client)
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    title='Flask Cli',
                    description='How to create cli project in flask?'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions/search/flask',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(resp.status_code, 200)

    def test_user_retrieves_user_search_results_if_none(self):
        """Test user search a none existing question"""
        with self.client:
            resp_register = register(self.client)
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    title='Flask Cli',
                    description='How to create cli project in flask?'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions/search/django',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'No results for your search')
            self.assertEqual(resp.status_code, 404)
