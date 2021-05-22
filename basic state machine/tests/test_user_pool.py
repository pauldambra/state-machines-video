import unittest

from IdentityProvider.UserPool import UserPool, SuccessfulLogin, FailedLogin, RegistrationFailed, RegistrationSucceeded


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

    def test_register_with_valid_credentials(self):
        registration_result = UserPool.register("valid", "valid")
        self.assertIsInstance(registration_result, RegistrationSucceeded)

    def test_register_with_invalid_credentials(self):
        registration_result = UserPool.register("anything else", "anything else")
        self.assertIsInstance(registration_result, RegistrationFailed)
