import unittest
from unittest.mock import Mock

from IdentityProvider.UserPool import LoginSucceeded, LoginFailed, RegistrationFailed, RegistrationSucceeded


class User:
    def __init__(self):
        self.subscribers = []
        self.state = "anonymous"
        self.failed_login_count = 0

    def transition(self, event):
        if isinstance(event, RegistrationSucceeded):
            self.state = "logged out"
        if self.state == "logged out" and isinstance(event, LoginSucceeded):
            self.state = "logged in"
        if isinstance(event, LoginFailed):
            self.failed_login_count += 1
            if self.failed_login_count > 3:
                self.state = "locked"
                for s in self.subscribers:
                    s.send_alert("user locked")

    def subscribe_to_locked_out(self, subscriber):
        self.subscribers.append(subscriber)


class Alerter:
    pass


class TellDontAsk(unittest.TestCase):

    def test_tell_me_what_I_need_to_know(self):
        """tell (me what I need to know) don't (make me) ask"""
        user = User()
        alerter = Alerter()
        alerter.send_alert = Mock()
        user.subscribe_to_locked_out(alerter)

        events = [
            RegistrationSucceeded(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed()
        ]
        for event in events:
            user.transition(event)

        alerter.send_alert.assert_called_once()



class TestUserAccount(unittest.TestCase):

    def test_registration_failed_leaves_user_anonymous(self):
        self.assert_user_transitions(
            [
                RegistrationFailed()
            ],
            "anonymous"
        )

    def test_registration_succeeded_leaves_user_logged_out(self):
        self.assert_user_transitions(
            [
                RegistrationSucceeded()
            ],
            "logged out"
        )

    def test_successful_login_leaves_user_logged_in(self):
        self.assert_user_transitions(
            [
                RegistrationSucceeded(),
                LoginSucceeded()
            ],
            "logged in"
        )

    def test_single_failed_login_leaves_user_logged_out(self):
        self.assert_user_transitions(
            [
                RegistrationSucceeded(),
                LoginFailed(),
            ],
            "logged out"
        )

    def test_three_failed_logins_leaves_user_logged_out(self):
        self.assert_user_transitions(
            [
                RegistrationSucceeded(),
                LoginFailed(),
                LoginFailed(),
                LoginFailed(),
            ],
            "logged out"
        )

    def test_four_failed_logins_leaves_user_locked(self):
        self.assert_user_transitions(
            [
                RegistrationSucceeded(),
                LoginFailed(),
                LoginFailed(),
                LoginFailed(),
                LoginFailed(),
            ],
            "locked"
        )

    def assert_user_transitions(self, events, final_state: str):
        user = User()
        for event in events:
            user.transition(event)
        self.assertEqual(user.state, final_state)
