from django.test import TestCase

from project_app.models import Notification

from classes.notification_class import NotificationClass
from classes.user_class import UserClass


class NotificationUnitTestSuite(TestCase):
    def setUp(self):
        self.sender = UserClass(
            username='sender', email='sender@uwm.edu', first_name='Test', last_name='Sender')
        self.sender.save_details()
        self.sender = self.sender.get_model_instance()

        self.recipient = UserClass(
            username='recipient', email='recipient@uwm.edu', first_name='Test', last_name='Recipient')
        self.recipient.save_details()
        self.recipient = self.recipient.get_model_instance()

        self.notification_class = NotificationClass(
            self.sender, self.recipient, 'Subject', 'Message')
        self.notification_class.save_details()

        self.invalid_class = NotificationClass(None, None, '', '')

    def test_init_default(self):
        notification_class = NotificationClass(
            self.sender, self.recipient, 'Subject', 'Message')

        self.assertEqual(notification_class.sender, self.sender)
        self.assertEqual(notification_class.recipient, self.recipient)
        self.assertEqual(notification_class.subject, 'Subject')
        self.assertEqual(notification_class.message, 'Message')
        self.assertEqual(notification_class.primary_key, None)
    
    def test_get_instance_default(self):
        notification_class = NotificationClass.get_instance(self.notification_class.get_model_instance())

        self.assertTrue(isinstance(notification_class, NotificationClass))

        self.assertEqual(notification_class.sender, self.notification_class.sender)
        self.assertEqual(notification_class.recipient, self.notification_class.recipient)
        self.assertEqual(notification_class.subject, self.notification_class.subject)
        self.assertEqual(notification_class.message, self.notification_class.message)
        self.assertEqual(notification_class.primary_key, self.notification_class.primary_key)

    def test_save_details_default(self):
        notification = Notification.objects.get(sender=self.sender, recipient=self.recipient)

        self.assertEqual(self.notification_class.sender, notification.sender)
        self.assertEqual(self.notification_class.recipient, notification.recipient)
        self.assertEqual(self.notification_class.subject, notification.subject)
        self.assertEqual(self.notification_class.message, notification.message)

    def test_save_details_duplicate(self):
        notification = Notification.objects.get(sender=self.sender, recipient=self.recipient)
        self.assertEqual(self.notification_class.primary_key, notification.id)

        self.notification_class.save_details()
        self.assertNotEqual(
            self.notification_class.primary_key, notification.id)

    def test_get_model_instance_default(self):
        notification = self.notification_class.get_model_instance()

        self.assertEqual(notification.id, self.notification_class.primary_key)
        self.assertEqual(notification.sender, self.notification_class.sender)
        self.assertEqual(notification.recipient,
                         self.notification_class.recipient)
        self.assertEqual(notification.subject, self.notification_class.subject)
        self.assertEqual(notification.message, self.notification_class.message)

    def test_get_model_instance_does_not_exist(self):
        with self.assertRaises(Notification.DoesNotExist, msg='get_model_instance does not raise Notification.DoesNotExist for non-existant notification'):
            self.invalid_class.get_model_instance()

    def test_get_sender_default(self):
        self.assertEqual(self.notification_class.get_sender(), self.sender)

    def test_get_recipient_default(self):
        self.assertEqual(
            self.notification_class.get_recipient(), self.recipient)

    def test_get_subject_default(self):
        self.assertEqual(self.notification_class.get_subject(), 'Subject')

    def test_get_message_default(self):
        self.assertEqual(self.notification_class.get_message(), 'Message')

    def test_get_primary_key_default(self):
        notification = self.notification_class.get_model_instance()
        self.assertEqual(
            self.notification_class.get_primary_key(), notification.id)
