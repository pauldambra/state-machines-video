import unittest

from IdentityProvider.UserPool import UserPool, SuccessfulLogin, FailedLogin


class TestUserPool(unittest.TestCase):

    def test_can_login_when_username_is_the_string_valid(self):
        login_result = UserPool.login("valid", "anything else")
        self.assertIsInstance(login_result, SuccessfulLogin)

    def test_can_login_when_password_is_the_string_valid(self):
        login_result = UserPool.login("anything else", "valid")
        self.assertIsInstance(login_result, SuccessfulLogin)

    def test_cannot_login_when_neither_username_nor_password_is_the_string_valid(self):
        login_result = UserPool.login("anything else", "anything else")
        self.assertIsInstance(login_result, FailedLogin)
