"""
Imports

"""
import json
from stackoverflow import settings
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

class TestAnswerResource(BaseTestCase):
    """Test answer resource"""
    def test_user_can_post_answer_to_a_question(self):
        """Test user can post an answer"""
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
            response_data = json.loads(resp.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Answer posted successfully')
            self.assertEqual(resp.status_code, 201)

    def test_user_can_upvote_an_answer_to_a_question(self):
        """Test user can upvote an answer"""
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
            resp = self.client.patch(
                '/api/v2/questions/1/answers/1/upvote',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(resp.status_code, 200)

    def test_user_can_down_vote_an_answer_to_a_question(self):
        """Test user can downvote an answer"""
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
            resp = self.client.patch(
                '/api/v2/questions/1/answers/1/downvote',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(resp.status_code, 200)

    def test_user_can_accept_an_answer_to_their_question(self):
        """test user can accept an answer"""
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
            resp = self.client.patch(
                '/api/v2/questions/1/answers/1/accept',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    accepted=settings.ACCEPT
                )),
                content_type='application/json'
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Answer accepted')
            self.assertEqual(resp.status_code, 200)
