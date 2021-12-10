from tests.test_main import BaseTestCase
from flask import request, session


class UserViewsTests(BaseTestCase):

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def register(self, username, password):
        return self.client.post('/register', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_not_existed_users_can_login(self):
        username = "test2"
        password = "123"
        response = self.login(username, password)
        self.assert_status(response, 400, message="Incorrect username.")

    def test_existed_users_can_login(self):
        username = "test"
        password = "123"
        user_id = 1

        response = self.login(username, password)
        self.assert_status(response, 200, message="OK")
        with self.client as c:
            rv = c.get('/')
            self.assertTrue(session["user_id"] == user_id)
            self.assertTrue(request.url, '/')

    def test_users_can_logout(self):
        username = "test"
        password = "123"
        user_id = 1

        response = self.login(username, password)
        with self.client as c:
            rv = c.get('/')
            self.assertTrue(session["user_id"] == user_id)
        response = self.logout()
        with self.client as c:
            rv = c.get('/')
            self.assertTrue(session == {})

    def test_existed_users_wrong_password_can_login(self):
        username = "test"
        password = "1234"
        response = self.login(username, password)
        self.assert_status(response, 400, message="Incorrect password.")

    def test_new_users_can_register(self):
        username = "test1"
        password = "123"
        user_id = 2
        response = self.register(username, password)
        self.assert_status(response, 200, message="OK")
        with self.client as c:
            rv = c.get('/')
            self.assertTrue(session["user_id"] == user_id)
            self.assertTrue(request.url, '/')

    def test_existed_users_cannot_register(self):
        username = "test"
        password = "123"
        response = self.register(username, password)
        self.assert_status(response, 400, message=f"User {username} is already registered.")
