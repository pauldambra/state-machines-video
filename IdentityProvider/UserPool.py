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

    @staticmethod
    def login(username, password):
        if username == "valid" or password == "valid":
            return SuccessfulLogin()
        else:
            return FailedLogin()

    @staticmethod
    def register(username, password):
        if username == "valid" or password == "valid":
            return RegistrationSucceeded()
        else:
            return RegistrationFailed()
