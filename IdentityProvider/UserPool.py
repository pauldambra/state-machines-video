from typing import List


# In a real user pool we might get lots of context about success or failure
class RegistrationSucceeded:
    pass


class RegistrationFailed:
    pass


class LoginSuccessful:
    pass


class LoginFailed:
    pass


class UserPool(object):
    users: List[str] = []

    @classmethod
    def login(cls, username, password):
        if username in cls.users and password == "valid":
            return LoginSuccessful()
        else:
            return LoginFailed()

    @classmethod
    def register(cls, username, password):
        if username not in cls.users:
            cls.users.append(username)
            return RegistrationSucceeded()
        else:
            return RegistrationFailed()
