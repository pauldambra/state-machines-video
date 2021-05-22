from typing import List


# In a real user pool we might get lots of context about success or failure
class RegistrationSucceeded:
    pass


class RegistrationFailed:
    pass


class SuccessfulLogin:
    pass


class FailedLogin:
    pass


class UserPool(object):
    users: List[str] = []

    @classmethod
    def login(cls, username, password):
        if username in cls.users and password == "valid":
            return SuccessfulLogin()
        else:
            return FailedLogin()

    @classmethod
    def register(cls, username, password):
        if username not in cls.users:
            cls.users.append(username)
            return RegistrationSucceeded()
        else:
            return RegistrationFailed()
