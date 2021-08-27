import unittest
from unittest.mock import Mock

from IdentityProvider.UserPool import LoginSucceeded, LoginFailed, RegistrationFailed, RegistrationSucceeded


class Anonymous:
    def transition(self, event):
        if isinstance(event, RegistrationSucceeded):
            return LoggedOut()
        else:
            return self


class LoggedOut:
    failed_login_count = 0

    def transition(self, event):
        if isinstance(event, LoginSucceeded):
            return LoggedIn()
        else:
            self.failed_login_count += 1
            if self.failed_login_count > 3:
                return Locked()
            else:
                return self


class LoggedIn:
    pass


class Locked:
    pass


class TestUserAccount(unittest.TestCase):

    def test_registration_failed_leaves_user_anonymous(self):
        self.assert_user_transitions(
            [
                RegistrationFailed()
            ],
            Anonymous
        )

    def test_registration_succeeded_leaves_user_logged_out(self):
        self.assert_user_transitions(
            [
                RegistrationSucceeded()
            ],
            LoggedOut
        )

    def test_successful_login_leaves_user_logged_in(self):
        self.assert_user_transitions(
            [
                RegistrationSucceeded(),
                LoginSucceeded()
            ],
            LoggedIn
        )

    def test_single_failed_login_leaves_user_logged_out(self):
        self.assert_user_transitions(
            [
                RegistrationSucceeded(),
                LoginFailed(),
            ],
            LoggedOut
        )

    def test_three_failed_logins_leaves_user_logged_out(self):
        self.assert_user_transitions(
            [
                RegistrationSucceeded(),
                LoginFailed(),
                LoginFailed(),
                LoginFailed(),
            ],
            LoggedOut
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
            Locked
        )

    def assert_user_transitions(self, events, final_state):
        state_machine = Anonymous()
        for event in events:
            state_machine = state_machine.transition(event)
        self.assertIsInstance(state_machine, final_state)
