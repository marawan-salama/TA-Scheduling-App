from django.test import TestCase
from project_app.models import Course, Section, User, Role
from classes.ta_class import TAClass


class TAUnitTestSuite(TestCase):
    def setUp(self):
        self.ta = User(username='ta', email='ta@uwm.edu',
                       first_name='Test', last_name='TA')
        self.ta.set_password('ta')
        self.ta.role = Role.TA
        self.ta.save()

        self.course = Course(name='Test', subject='TEST', number='001')
        self.course.save()

        self.ta.courses.add(self.course)
        self.ta.save()

        self.section = Section(number='001', course=self.course)
        self.section.save()

        self.section.tas.add(self.ta)
        self.section.save()

        self.ta_class = TAClass(username='ta', email='ta@uwm.edu', first_name='Test',
                                last_name='TA', phone_number='', home_address='', courses=[self.course])

    def test_init_default(self):
        ta_class = TAClass(username='ta', email='ta@uwm.edu', first_name='Test',
                           last_name='TA', phone_number='', home_address='', courses=[self.course])

        self.assertEqual(ta_class.username, 'ta')
        self.assertEqual(ta_class.email, 'ta@uwm.edu')
        self.assertEqual(ta_class.first_name, 'Test')
        self.assertEqual(ta_class.last_name, 'TA')
        self.assertEqual(ta_class.role, Role.TA)
        self.assertEqual(ta_class.phone_number, '')
        self.assertEqual(ta_class.home_address, '')
        self.assertEqual(ta_class.courses, [self.course])

    def test_get_sections_default(self):
        ta_class = TAClass(username='ta', email='ta@uwm.edu', first_name='Test',
                           last_name='TA', phone_number='', home_address='', courses=[self.course])
        sections = ta_class.get_sections()
        self.assertEqual(list(sections), [self.section])

    def test_get_sections_does_not_exist(self):
        ta_class = TAClass(username='non_existent', email='non_existent@uwm.edu', first_name='Test',
                           last_name='TA', phone_number='', home_address='', courses=[self.course])
        with self.assertRaises(User.DoesNotExist, msg='get_tas does not throw section does not exist'):
            ta_class.get_sections()

    def test_has_section_true(self):
        ta_class = TAClass(username='ta', email='ta@uwm.edu', first_name='Test',
                           last_name='TA', phone_number='', home_address='', courses=[self.course])
        has_section = ta_class.has_section(self.section)
        self.assertTrue(has_section)

    def test_has_section_false(self):
        ta_class = TAClass(username='ta', email='ta@uwm.edu', first_name='Test',
                           last_name='TA', phone_number='', home_address='', courses=[self.course])
        new_section = Section(number='002', course=self.course)
        new_section.save()
        has_section = ta_class.has_section(new_section)
        self.assertFalse(has_section)

    def test_has_section_does_not_exist(self):
        ta_class = TAClass(username='non_existent', email='non_existent@uwm.edu', first_name='Test',
                           last_name='TA', phone_number='', home_address='', courses=[self.course])
        with self.assertRaises(User.DoesNotExist, msg='get_tas does not throw section does not exist'):
            ta_class.has_section(self.section)