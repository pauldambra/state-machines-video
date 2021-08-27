import unittest
from unittest.mock import Mock

from IdentityProvider.UserPool import LoginSucceeded, LoginFailed, RegistrationFailed, RegistrationSucceeded


class EventStream:
    def __init__(self):
        self.subscribers = {}
        self.subscribe_all = []

    def send(self, event):
        event_type = str(type(event))
        for subscriber in self.subscribers.get(event_type, []):
            subscriber.send(event)

        for subscriber in self.subscribe_all:
            subscriber.send(event)

    def subscribe(self, event_type, subscriber):
        self.subscribers[str(event_type)] = [subscriber]

    def subscribe_to_all(self, subscriber):
        self.subscribe_all.append(subscriber)


class UserLockedOut:
    pass


class User:
    def __init__(self, event_stream: EventStream):
        self.event_stream = event_stream
        self.event_stream.subscribe_to_all(self)
        self.state = "anonymous"
        self.failed_login_count = 0

    def send(self, event):
        if isinstance(event, RegistrationSucceeded):
            self.state = "logged out"
        if self.state == "logged out" and isinstance(event, LoginSucceeded):
            self.state = "logged in"
        if isinstance(event, LoginFailed):
            self.failed_login_count += 1
            if self.failed_login_count > 3:
                self.state = "locked"
                self.event_stream.send(UserLockedOut())


class Alerter:
    pass


class TellDontAsk(unittest.TestCase):

    def test_event_stream(self):
        event_stream = EventStream()
        user = User(event_stream)

        alerter = Alerter()
        alerter.send = Mock()
        event_stream.subscribe(UserLockedOut, alerter)

        events = [
            RegistrationSucceeded(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed()
        ]
        for event in events:
            event_stream.send(event)

        self.assertEqual(user.state, "locked")
        alerter.send.assert_called_once()


    # def test_tell_me_what_I_need_to_know(self):
    #     """tell (me what I need to know) don't (make me) ask"""
    #     user = User()
    #     alerter = Alerter()
    #     alerter.send_alert = Mock()
    #     user.subscribe_to_locked_out(alerter)
    #
    #     events = [
    #         RegistrationSucceeded(),
    #         LoginFailed(),
    #         LoginFailed(),
    #         LoginFailed(),
    #         LoginFailed()
    #     ]
    #     for event in events:
    #         user.transition(event)
    #
    #     alerter.send_alert.assert_called_once()



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
