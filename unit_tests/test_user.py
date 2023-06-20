from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from project_app.models import Course, Section, Notification, User, Role

from classes.user_class import UserClass
from classes.course_class import CourseClass
from classes.section_class import SectionClass
from classes.notification_class import NotificationClass


class UserUnitTestSuite(TestCase):
    def setUp(self):
        self.user_class = UserClass(username='user', email='user@uwm.edu', first_name='Test', last_name='User')
        self.user_class.save_details()

        self.test_class = UserClass(username='test', email='test@uwm.edu', first_name='Test', last_name='Test')
        self.test_class.save_details()

        self.invalid_class = UserClass(username='invalid', email='invalid@uwm.edu', first_name='Test', last_name='Invalid')

        self.course = CourseClass(name='Test', subject='TEST', number='001')
        self.course.save_details()
        self.course = self.course.get_model_instance()

        self.section = SectionClass(number='001', course=self.course)
        self.section.save_details()
        self.section = self.section.get_model_instance()

        self.notification = NotificationClass(self.user_class.get_model_instance(), self.test_class.get_model_instance(), 'Subject', 'Message')
        self.notification.save_details()
        self.notification = self.notification.get_model_instance()

        self.user_class.sent_notifications = [self.notification]
        self.test_class.received_notifications = [self.notification]

        user = self.user_class.get_model_instance()
        user.sent_notifications.add(self.notification)

        test = self.test_class.get_model_instance()
        test.received_notifications.add(self.notification)

    def test_init_default(self):
        user_class = UserClass(username='user', email='user@uwm.edu', first_name='Test', last_name='User', role=Role.TA, phone_number='', home_address='', courses=[self.course])

        self.assertEqual(user_class.username, 'user')
        self.assertEqual(user_class.email, 'user@uwm.edu')
        self.assertEqual(user_class.first_name, 'Test')
        self.assertEqual(user_class.last_name, 'User')
        self.assertEqual(user_class.role, Role.TA)
        self.assertEqual(user_class.phone_number, '')
        self.assertEqual(user_class.home_address, '')
        self.assertEqual(user_class.courses, [self.course])
        self.assertEqual(user_class.sent_notifications, [])
        self.assertEqual(user_class.received_notifications, [])

    def test_validate_default(self):
        pass

    def test_save_details_default(self):
        user = User.objects.get(username=self.user_class.username)

        self.assertEqual(self.user_class.username, user.username)
        self.assertEqual(self.user_class.email, user.email)
        self.assertEqual(self.user_class.first_name, user.first_name)
        self.assertEqual(self.user_class.last_name, user.last_name)
        self.assertEqual(self.user_class.role, user.role)
        self.assertEqual(self.user_class.phone_number, user.phone_number)
        self.assertEqual(self.user_class.home_address, user.home_address)
        self.assertEqual(self.user_class.courses, list(user.courses.all()))

    def test_save_details_exists(self):
        with self.assertRaises(IntegrityError, msg='Failed to raise IntegrityError for duplicate user'):
            self.user_class.save_details()
    
    def test_get_model_instance_default(self):
        user = self.user_class.get_model_instance()

        self.assertEqual(user.username, self.user_class.username)
        self.assertEqual(user.email, self.user_class.email)
        self.assertEqual(user.first_name, self.user_class.first_name)
        self.assertEqual(user.last_name, self.user_class.last_name)
        self.assertEqual(user.role, self.user_class.role)
        self.assertEqual(user.phone_number, self.user_class.phone_number)
        self.assertEqual(user.home_address, self.user_class.home_address)
        self.assertEqual(list(user.courses.all()), self.user_class.courses)
        self.assertEqual(list(user.sent_notifications.all()), self.user_class.sent_notifications)
        self.assertEqual(list(user.received_notifications.all()), self.user_class.received_notifications)

    def test_get_model_instance_does_not_exist(self):
        with self.assertRaises(User.DoesNotExist, msg='get_model_instance does not throw user does not exist exception'):
            self.invalid_class.get_model_instance()
    
    def test_get_instance_default(self):
        user_class = UserClass.get_instance(self.user_class.get_model_instance())

        self.assertTrue(isinstance(user_class, UserClass))

        self.assertEqual(user_class.username, self.user_class.username)
        self.assertEqual(user_class.email, self.user_class.email)
        self.assertEqual(user_class.first_name, self.user_class.first_name)
        self.assertEqual(user_class.last_name, self.user_class.last_name)
        self.assertEqual(user_class.role, self.user_class.role)
        self.assertEqual(user_class.phone_number, self.user_class.phone_number)
        self.assertEqual(user_class.home_address, self.user_class.home_address)
        self.assertEqual(user_class.courses, self.user_class.courses)
        self.assertEqual(user_class.sent_notifications, self.user_class.sent_notifications)
        self.assertEqual(user_class.received_notifications, self.user_class.received_notifications)
    
    def test_delete_default(self):
        self.user_class.delete()

        with self.assertRaises(User.DoesNotExist, msg='Failed to delete the user from db'):
            self.user_class.get_model_instance()
    
    def test_delete_does_not_exist(self):
        self.user_class.delete()

        with self.assertRaises(User.DoesNotExist, msg='delete does not raise User.DoesNotExist for non-existant user'):
            self.user_class.delete()

    def test_get_username_default(self):
        self.assertEqual(self.user_class.get_username(), 'user')

    def test_set_username_default(self):
        self.user_class.set_username('testuser')
        self.assertEqual(self.user_class.username, 'testuser')

        user = self.user_class.get_model_instance()
        self.assertEqual(user.username, 'testuser')

    def test_get_email_default(self):
        self.assertEqual(self.user_class.get_email(), 'user@uwm.edu')

    def test_set_email_default(self):
        self.user_class.set_email('testuser@uwm.edu')
        self.assertEqual(self.user_class.email, 'testuser@uwm.edu')

        user = self.user_class.get_model_instance()
        self.assertEqual(user.email, 'testuser@uwm.edu')

    def test_get_first_name(self):
        self.assertEqual(self.user_class.get_first_name(), 'Test')

    def test_set_first_name_default(self):
        self.user_class.set_first_name('test')
        self.assertEqual(self.user_class.first_name, 'test')

        user = self.user_class.get_model_instance()
        self.assertEqual(user.first_name, 'test')

    def test_get_last_name(self):
        self.assertEqual(self.user_class.get_last_name(), 'User')

    def test_set_last_name_default(self):
        self.user_class.set_last_name('user')
        self.assertEqual(self.user_class.last_name, 'user')

        user = self.user_class.get_model_instance()
        self.assertEqual(user.last_name, 'user')

    def test_get_role_default(self):
        self.assertEqual(self.user_class.get_role(), None)

    def test_set_role_default(self):
        self.user_class.set_role(Role.TA)
        self.user_class.role = Role.TA

        user = self.user_class.get_model_instance()
        self.assertEqual(user.role, Role.TA)

    def test_set_password_default(self):
        self.user_class.set_password('foobar123')
        
        user = self.user_class.get_model_instance()
        self.assertTrue(user.check_password('foobar123'))

    def test_set_password_invalid(self):
        with self.assertRaises(ValidationError, msg='set_password does not raise ValidationError for invalid password'):
            self.user_class.set_password('password')

    def test_set_phone_number_default(self):
        self.user_class.set_phone_number('123456789123')
        self.assertEqual(self.user_class.phone_number, '123456789123')

        user = self.user_class.get_model_instance()
        self.assertEqual(user.phone_number, '123456789123')

    def test_set_home_address_default(self):
        self.user_class.set_home_address('123 Main St.')
        self.assertEqual(self.user_class.home_address, '123 Main St.')

        user = User.objects.get(username=self.user_class.username)
        self.assertEqual(user.home_address, '123 Main St.')

    def test_add_course_default(self):
        self.user_class.add_course(self.course)
        self.assertIn(self.course, self.user_class.courses)

        user = User.objects.get(username=self.user_class.username)
        self.assertIn(self.course, user.courses.all())
    
    def test_add_course_exists(self):
        self.user_class.add_course(self.course)
        self.assertNotEqual(self.user_class.courses, [self.course, self.course])

        user = self.user_class.get_model_instance()
        self.assertNotEqual(list(user.courses.all()), [self.course, self.course])

    def test_get_courses_default(self):
        user = self.user_class.get_model_instance()
        user.courses.add(self.course)
        user.save()

        self.assertEqual(list(self.user_class.get_courses()), [self.course])

    def test_get_courses_empty(self):
        self.assertEqual(list(self.user_class.get_courses()), [])

    def test_has_course_true(self):
        self.user_class.add_course(self.course)

        user = self.user_class.get_model_instance()

        self.assertTrue(user.courses.filter(subject=self.course.subject, number=self.course.number).exists())
        self.assertTrue(self.user_class.has_course(self.course))

    def test_has_course_false(self):
        user = self.user_class.get_model_instance()

        self.assertFalse(user.courses.filter(subject=self.course.subject, number=self.course.number).exists())
        self.assertFalse(self.user_class.has_course(self.course))

    def test_get_received_notifications_default(self):
        self.assertEqual(list(self.test_class.get_received_notifications()), [self.notification])

    def test_get_received_notifications_empty(self):
        self.assertEqual(list(self.user_class.get_received_notifications()), [])
    
    def test_is_supervisor_default(self):
        self.user_class.set_role(Role.SUPERVISOR)

        self.assertTrue(self.user_class.is_supervisor())
        self.assertFalse(self.user_class.is_instructor())
        self.assertFalse(self.user_class.is_ta())

    def test_is_instructor_default(self):
        self.user_class.set_role(Role.INSTRUCTOR)

        self.assertFalse(self.user_class.is_supervisor())
        self.assertTrue(self.user_class.is_instructor())
        self.assertFalse(self.user_class.is_ta())

    def test_is_ta_default(self):
        self.user_class.set_role(Role.TA)
        self.assertFalse(self.user_class.is_supervisor())
        self.assertFalse(self.user_class.is_instructor())
        self.assertTrue(self.user_class.is_ta())

    def test_all_default(self):
        self.assertIn(self.user_class.get_model_instance(), list(UserClass.all()))
        self.assertIn(self.test_class.get_model_instance(), list(UserClass.all()))
