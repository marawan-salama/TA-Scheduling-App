from django.test import TestCase
from django.db.utils import IntegrityError

from project_app.models import Course, Section, User, Role

from classes.section_class import SectionClass
from classes.course_class import CourseClass
from classes.instructor_class import InstructorClass
from classes.ta_class import TAClass


class SectionUnitTestSuite(TestCase):
    def setUp(self):
        self.instructor = InstructorClass(username='instructor', email='instructor@uwm.edu',
                               first_name='Test', last_name='Instructor')
        self.instructor.save_details()
        self.instructor = self.instructor.get_model_instance()

        self.ta = TAClass(username='ta', email='ta@uwm.edu',
                       first_name='Test', last_name='TA')
        self.ta.save_details()
        self.ta = self.ta.get_model_instance()

        self.course = CourseClass(name='Test', subject='TEST',
                             number='001', instructor=self.instructor)
        self.course.save_details()
        self.course = self.course.get_model_instance()

        self.section_class = SectionClass('1', self.course)
        self.section_class.save_details()

        self.invalid_class = SectionClass('', course=None)

    def test_init_default(self):
        section_class = SectionClass('1', self.course, [self.ta])

        self.assertEqual(section_class.number, '1')
        self.assertEqual(section_class.course, self.course)
        self.assertEqual(section_class.ta, self.ta)

    def test_save_details_default(self):
        section = Section.objects.get(number=self.section_class.number, course=self.section_class.course)

        self.assertEqual(self.section_class.number, section.number)
        self.assertEqual(self.section_class.course, section.course)
        self.assertEqual(self.section_class.ta, section.ta)

    def test_save_details_exists(self):
        with self.assertRaises(IntegrityError, msg='save_details does not raise IntegrityError for duplicate section'):
            self.section_class.save_details()

    def test_get_model_instance_default(self):
        section = self.section_class.get_model_instance()

        self.assertEqual(section.number, self.section_class.number)
        self.assertEqual(section.course, self.section_class.course)
        self.assertEqual(section.ta, self.section_class.ta)
    
    def test_get_model_instance_does_not_exist(self):
        with self.assertRaises(Section.DoesNotExist, msg='get_model_instance does not raise Section.DoesNotExist for non-existant section'):
            self.invalid_class.get_model_instance()

    def test_get_instance_default(self):
        section_class = SectionClass.get_instance(self.section_class.get_model_instance())

        self.assertTrue(isinstance(section_class, SectionClass))

        self.assertEqual(section_class.number, self.section_class.number)
        self.assertEqual(section_class.course, self.section_class.course)
        self.assertEqual(section_class.tas, self.section_class.tas)

    def test_delete_default(self):
        self.section_class.delete()
        with self.assertRaises(Section.DoesNotExist, msg='Failed to delete the section from db'):
            Section.objects.get(number=self.section_class.number, course=self.section_class.course)

    def test_delete_does_not_exist(self):
        self.section_class.delete()

        with self.assertRaises(Section.DoesNotExist, msg='delete does not raise Section.DoesNotExist for non-existant section'):
            self.section_class.delete()

    def test_get_number(self):
        self.assertEqual(self.section_class.get_number(), '1')

    def test_set_number(self):
        self.section_class.set_number('2')
        self.assertEqual(self.section_class.number, '2')

        section = self.section_class.get_model_instance()
        self.assertEqual(section.number, '2')

    def test_get_course(self):
        self.assertEqual(self.section_class.get_course(), self.course)

    def test_add_ta_default(self):
        ta_2 = TAClass(username='ta_2', email='ta_2@uwm.edu',
                    first_name='Test2', last_name='TA2')
        ta_2.save_details()
        ta_2 = ta_2.get_model_instance()

        self.section_class.set_ta(ta_2)
        self.assertIn(ta_2, self.section_class.ta)

        section = self.section_class.get_model_instance()
        self.assertIn(ta_2, section.tas.all())

        self.assertIn(self.section_class.get_course(), ta_2.courses.all())

    def test_set_ta_does_not_exist(self):
        invalid_ta = User(username='invalid', email='invalid@uwm.edu',
                       first_name='Test', last_name='Invalid')
        invalid_ta.set_password('invalid')
        invalid_ta.role = Role.TA

        with self.assertRaises(ValueError, msg='set_ta does not raise ValueError for non-existent TA'):
            self.section_class.set_ta(invalid_ta)
