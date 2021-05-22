
class SuccessfulLogin:
    pass


class FailedLogin:
    pass


class UserPool(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserPool, cls).__new__(cls)
        return cls._instance

    def login(self, username, password):
        if username == "valid" or password == "valid":
            return SuccessfulLogin()
        else:
            return FailedLogin()
