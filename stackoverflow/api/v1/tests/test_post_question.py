"""
Imports

"""

import json
from stackoverflow import settings
from .base_test import BaseTestCase

class TestUserQuestions(BaseTestCase):
    """Testing user can create a question"""
    def test_post_question(self):
        """Test user can post a new question"""
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='Brian Mboya',
                    email='asheuh@gmail.com',
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    title='Gjango cli',
                    description='How to create cli project in django?'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Question posted successfully')
            self.assertEqual(response.status_code, 201)

    def test_user_retrieves_one_question(self):
        """Test user can retrieve one question"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    title='Gjango cli',
                    description='How to create cli project in django?'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v1/questions/3',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(resp.status_code, 200)

    def test_user_retrieves_all_questions(self):
        """Test user can retrieve all the questions"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v1/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(resp.status_code, 200)

    def test_user_retrieves_one_question_if_none_with_that_id_in_the_db(self):
        """Test user Cannot retrieve a none question"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v1/questions/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['message'] == 'Question with id 1 doesn\'t exist')
            self.assertEqual(resp.status_code, 404)

    def test_user_can_delete_their_question(self):
        """Test user ca delete their question"""
        with self.client:
            resp_register = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    name='Ivy Mboya',
                    email='ivy@gmail.com',
                    username='ivy',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/questions',
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
            resp = self.client.delete(
                '/api/v1/questions/2',
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

    def test_user_cannot_delete_other_users_questions(self):
        """Test user cannot delete others questions"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='ivy',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            resp = self.client.delete(
                '/api/v1/questions/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'You are not permitted to delete this question')
            self.assertEqual(resp.status_code, 401)

    def test_user_can_post_answer_to_a_question(self):
        """Test user can post an answer to a question"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='ivy',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            resp = self.client.post(
                '/api/v1/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    answer='Use click'
                )),
                content_type='application/json'
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Answer posted successfully')
            self.assertEqual(resp.status_code, 201)

    def test_user_get_all_answers_to_a_question(self):
        """Test user can get all the answers to a question"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='ivy',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v1/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(resp.status_code, 200)

    def test_user_can_accept_an_answer_to_their_question(self):
        """test user ca accept an answer"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    answer='Use click cli'
                )),
                content_type='application/json'
            )
            resp = self.client.patch(
                '/api/v1/questions/1/answers/1/accept',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
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

    def test_user_can_upvote_an_answer_to_a_question(self):
        """Test user can upvote an answer"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    answer='Use click cli'
                )),
                content_type='application/json'
            )
            resp = self.client.patch(
                '/api/v1/questions/1/answers/1/upvote',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'You upvoted this answer, thanks for the feedback')
            self.assertEqual(resp.status_code, 200)

    def test_user_can_downvote_an_answer_to_a_question(self):
        """Test user can downvote an answer"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    answer='Use click cli'
                )),
                content_type='application/json'
            )
            resp = self.client.patch(
                '/api/v1/questions/1/answers/1/downvote',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'You down voted this answer, thanks for the feedback')
            self.assertEqual(resp.status_code, 200)

    def test_user_retrieves_all_questions_if_none(self):
        """Test user cannont Retrieve nonoe questions"""
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            resp = self.client.delete(
                '/api/v1/questions/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            resp = self.client.get(
                '/api/v1/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['Authorization']['access_token']
                )
            )
            response_data = json.loads(resp.data.decode())
            print(response_data)
            self.assertTrue(response_data['status'] == 'fail')
            self.assertEqual(resp.status_code, 404)
