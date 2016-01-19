import base64
import unittest

from flask.ext.testing import TestCase
from mongoengine.connection import get_connection
from api import app


class UserTestCase(TestCase):
    user1 = {
        'username': 'michaelbukachi',
        'password': 'dance',
        'type': 'individual'
    }

    user2 = {
        'username': 'robertbonnke',
        'password': 'sing',
        'type': 'individual'
    }

    user3 = {
        'username': 'dita',
        'password': 'dita',
        'type': 'group'
    }

    def create_app(self):
        return app

    def setUp(self):
        pass

    def tearDown(self):
        connection = get_connection()
        connection.drop_database('memo_test')

    def test_user_post(self):
        response = self.client.post('/api/v1/users')
        self.assert400(response)
        response = self.client.post('/api/v1/users', data=self.user1)
        self.assert200(response)

    def test_user_get(self):
        response = self.client.get('/api/v1/users')
        self.assertEquals(response.json, dict())
        response = self.client.get('/api/v1/users/sdfsdf')
        self.assert404(response)
        self.client.post('/api/v1/users', data=self.user1)
        self.client.post('/api/v1/users', data=self.user2)
        self.client.post('/api/v1/users', data=self.user3)
        response = self.client.get('/api/v1/users/{}'.format(self.user1['username']))
        self.assertEquals(self.user1['username'], response.json['username'])
        response = self.client.get('/api/v1/users')
        self.assertEquals(len(response.json.keys()), 3)

    def test_user_put(self):
        self.client.post('/api/v1/users', data=self.user1)
        response = self.client.put('/api/v1/users/{}'.format(self.user1['username']), data={
            'username': 'michaelbukachi',
            'password': 'dancer'
        })
        self.assert200(response)

    def test_user_delete(self):
        self.client.post('/api/v1/users', data=self.user1)
        response = self.client.delete('/api/v1/users/{}'.format(self.user1['username']))
        self.assertEquals(response.json, dict(message='deleted'))
        response = self.client.get('/api/v1/users')
        self.assertEquals(response.json, dict())

    def test_user_authentication(self):
        self.client.post('/api/v1/users', data=self.user1)
        response = self.client.post('/api/v1/users/authenticate', data={
            'username': 'michaelbukachi',
            'password': 'dancer'
        })
        self.assert401(response)
        response = self.client.post('/api/v1/users/authenticate', data={
            'username': 'michaelbukachi',
            'password': 'dance'
        })
        self.assert200(response)


    def open(self, url, method, credentials):
        return self.client.open(url, method=method, headers={
            'Authorization': 'Basic ' +
                             base64.b64encode(bytes(credentials[0] + ':' + credentials[1], 'ascii')).decode('ascii')
        })


if __name__ == '__main__':
    unittest.main()
