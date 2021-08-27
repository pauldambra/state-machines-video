import unittest
import random
import string

from IdentityProvider.UserPool import UserPool, LoginFailed, LoginSucceeded, RegistrationSucceeded, RegistrationFailed


def any_string(length: int = 10) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class TestUserPool(unittest.TestCase):

    def test_cannot_login_before_registration(self):
        login_result = UserPool.login("new user", "valid")
        self.assertIsInstance(login_result, LoginFailed)

    def test_can_login_when_registered_and_the_password_is_the_string_valid(self):
        UserPool.register("a user", "valid")
        login_result = UserPool.login("a user", "valid")
        self.assertIsInstance(login_result, LoginSucceeded)

    def test_cannot_login_when_password_is_not_the_string_valid(self):
        UserPool.register("a user", "valid")
        login_result = UserPool.login("a user", "anything else")
        self.assertIsInstance(login_result, LoginFailed)

    def test_register_with_valid_credentials(self):
        registration_result = UserPool.register(any_string(), "valid")
        self.assertIsInstance(registration_result, RegistrationSucceeded)

    def test_registration_fails_for_a_known_bad_user(self):
        registration_result = UserPool.register("should not register", "valid")
        self.assertIsInstance(registration_result, RegistrationFailed)

    def test_cannot_register_twice(self):
        username = any_string()
        UserPool.register(username, any_string())
        registration_result = UserPool.register(username, any_string())
        self.assertIsInstance(registration_result, RegistrationFailed)
