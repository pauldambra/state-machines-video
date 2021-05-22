
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
