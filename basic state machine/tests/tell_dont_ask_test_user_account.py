import unittest
from unittest.mock import Mock

from IdentityProvider.UserPool import LoginSucceeded, LoginFailed, RegistrationFailed, RegistrationSucceeded

import uuid

"""
the next thing to do is to store the events
and to let a client be able to 
  * read forwards from an event
  * read backwards from an event
  * to specify the expected next event  
"""

class EventStore:
    def __init__(self):
        self.stream_subscriptions = {}

    def send(self, event, stream_name: str):
        for subscriber in self.stream_subscriptions.get(stream_name, []):
            subscriber.send(event)

        event_type = type(event).__name__
        for subscriber in self.stream_subscriptions.get(event_type, []):
            subscriber.send(event)

    def subscribe(self, stream_name: str, subscriber):
        if stream_name not in self.stream_subscriptions.keys():
            self.stream_subscriptions[stream_name] = []

        self.stream_subscriptions[stream_name].append(subscriber)


class UserLockedOut:
    pass


class User:
    def __init__(self, event_stream: EventStore, user_id: uuid = None):
        self.event_stream = event_stream
        self.user_id = user_id
        self.stream_name = "User-" + str(self.user_id)
        self.event_stream.subscribe(self.stream_name, self)
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
                self.event_stream.send(UserLockedOut(), self.stream_name)


class Alerter:
    pass


class TellDontAsk(unittest.TestCase):

    def setUp(self):
        self.event_store = EventStore()

    def write_to_stream(self, stream_name: str, events):
        es = events
        for event in es:
            self.event_store.send(event, stream_name)

    def test_can_have_more_than_one_user(self):
        user_one_id = uuid.uuid4()
        user_one = User(self.event_store, user_one_id)

        user_two_id = uuid.uuid4()
        user_two = User(self.event_store, user_two_id)

        alerter = Alerter()
        alerter.send = Mock()
        self.event_store.subscribe("UserLockedOut", alerter)

        self.write_to_stream("User-" + str(user_one_id), [
            RegistrationSucceeded(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed(),
        ])

        self.assertNotEqual(user_one.state, "locked")
        alerter.send.assert_not_called()

        self.write_to_stream("User-" + str(user_two_id), [
            RegistrationSucceeded(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed()
        ])

        self.assertEqual(user_two.state, "locked")
        self.assertNotEqual(user_one.state, "locked")

    def test_user_stays_up_to_date(self):
        user_id = uuid.uuid4()
        user = User(self.event_store, user_id)

        alerter = Alerter()
        alerter.send = Mock()
        self.event_store.subscribe("UserLockedOut", alerter)

        self.write_to_stream("User-" + str(user_id), [
            RegistrationSucceeded(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed(),
        ])

        self.assertNotEqual(user.state, "locked")
        alerter.send.assert_not_called()

        self.write_to_stream("User-" + str(user_id), [
            LoginFailed(),
        ])

        self.assertEqual(user.state, "locked")
        alerter.send.assert_called_once()

    def test_event_stream(self):
        user_id = uuid.uuid4()
        user = User(self.event_store, user_id)

        alerter = Alerter()
        alerter.send = Mock()
        self.event_store.subscribe("UserLockedOut", alerter)

        self.write_to_stream("User-" + str(user_id), [
            RegistrationSucceeded(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed(),
            LoginFailed()
        ])

        self.assertEqual(user.state, "locked")
        alerter.send.assert_called_once()


    # def test_tell_me_what_I_need_to_know(self):
    #     """tell (me what I need to know) don't (make me) ask"""
    #     user_one = User()
    #     alerter = Alerter()
    #     alerter.send_alert = Mock()
    #     user_one.subscribe_to_locked_out(alerter)
    #
    #     events = [
    #         RegistrationSucceeded(),
    #         LoginFailed(),
    #         LoginFailed(),
    #         LoginFailed(),
    #         LoginFailed()
    #     ]
    #     for event in events:
    #         user_one.transition(event)
    #
    #     alerter.send_alert.assert_called_once()



# class TestUserAccount(unittest.TestCase):
#
#     def test_registration_failed_leaves_user_anonymous(self):
#         self.assert_user_transitions(
#             [
#                 RegistrationFailed()
#             ],
#             "anonymous"
#         )
#
#     def test_registration_succeeded_leaves_user_logged_out(self):
#         self.assert_user_transitions(
#             [
#                 RegistrationSucceeded()
#             ],
#             "logged out"
#         )
#
#     def test_successful_login_leaves_user_logged_in(self):
#         self.assert_user_transitions(
#             [
#                 RegistrationSucceeded(),
#                 LoginSucceeded()
#             ],
#             "logged in"
#         )
#
#     def test_single_failed_login_leaves_user_logged_out(self):
#         self.assert_user_transitions(
#             [
#                 RegistrationSucceeded(),
#                 LoginFailed(),
#             ],
#             "logged out"
#         )
#
#     def test_three_failed_logins_leaves_user_logged_out(self):
#         self.assert_user_transitions(
#             [
#                 RegistrationSucceeded(),
#                 LoginFailed(),
#                 LoginFailed(),
#                 LoginFailed(),
#             ],
#             "logged out"
#         )
#
#     def test_four_failed_logins_leaves_user_locked(self):
#         self.assert_user_transitions(
#             [
#                 RegistrationSucceeded(),
#                 LoginFailed(),
#                 LoginFailed(),
#                 LoginFailed(),
#                 LoginFailed(),
#             ],
#             "locked"
#         )
#
#     def assert_user_transitions(self, events, final_state: str):
#         user = User()
#         for event in events:
#             user.transition(event)
#         self.assertEqual(user.state, final_state)
