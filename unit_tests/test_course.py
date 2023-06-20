from django.test import TestCase
from django.db.utils import IntegrityError

from project_app.models import Course, User, Role

from classes.course_class import CourseClass
from classes.instructor_class import InstructorClass
from classes.ta_class import TAClass


class CourseUnitTestSuite(TestCase):
    def setUp(self):
        self.instructor = InstructorClass(username='instructor', email='instructor@uwm.edu',
                                          first_name='Test', last_name='Instructor')
        self.instructor.save_details()
        self.instructor = self.instructor.get_model_instance()

        self.ta = TAClass(username='ta', email='ta@uwm.edu',
                          first_name='Test', last_name='TA')
        self.ta.save_details()
        self.ta = self.ta.get_model_instance()

        self.course_class = CourseClass(
            'COURSE', '1', 'Course', self.instructor)
        self.course_class.save_details()

        self.invalid_class = CourseClass('INVALID', '1')

    def test_init_default(self):
        course_class = CourseClass('COURSE', '1', 'Course', self.instructor)

        self.assertEqual(course_class.subject, 'COURSE')
        self.assertEqual(course_class.number, '1')
        self.assertEqual(course_class.name, 'Course')
        self.assertEqual(course_class.instructor, self.instructor)

    def test_save_details_default(self):
        course = Course.objects.get(
            subject=self.course_class.subject, number=self.course_class.number)

        self.assertEqual(self.course_class.subject, course.subject)
        self.assertEqual(self.course_class.number, course.number)
        self.assertEqual(self.course_class.name, course.name)
        self.assertEqual(self.course_class.instructor, course.instructor)

    def test_save_details_exists(self):
        with self.assertRaises(IntegrityError, msg='save_details does not raise IntegrityError for duplicate course'):
            self.course_class.save_details()

    def test_get_model_instance(self):
        course = self.course_class.get_model_instance()

        self.assertEqual(course.subject, self.course_class.subject)
        self.assertEqual(course.number, self.course_class.number)
        self.assertEqual(course.name, self.course_class.name)
        self.assertEqual(course.instructor, self.course_class.instructor)

    def test_get_model_instance_does_not_exist(self):
        with self.assertRaises(Course.DoesNotExist, msg='get_model_instance does not raise Course.DoesNotExist for non-existant course'):
            self.invalid_class.get_model_instance()

    def test_get_instance_default(self):
        course_class = CourseClass.get_instance(
            self.course_class.get_model_instance())

        self.assertTrue(isinstance(course_class, CourseClass))

        self.assertEqual(course_class.subject, self.course_class.subject)
        self.assertEqual(course_class.number, self.course_class.number)
        self.assertEqual(course_class.name, self.course_class.name)
        self.assertEqual(course_class.instructor, self.course_class.instructor)

    def test_delete_default(self):
        self.course_class.delete()

        with self.assertRaises(Course.DoesNotExist, msg='Failed to delete the course from db'):
            self.course_class.get_model_instance()

    def test_delete_does_not_exist(self):
        self.course_class.delete()

        with self.assertRaises(Course.DoesNotExist, msg='delete does not raise Course.DoesNotExist for non-existant course'):
            self.course_class.delete()

    def test_get_subject_default(self):
        self.assertEqual(self.course_class.get_subject(), 'COURSE')

    def test_set_subject_default(self):
        self.course_class.set_subject('TEST')
        self.assertEqual(self.course_class.subject, 'TEST')

        course = self.course_class.get_model_instance()

        self.assertEqual(course.subject, 'TEST')

    def test_get_number_default(self):
        self.assertEqual(self.course_class.get_number(), '1')

    def test_set_number_default(self):
        self.course_class.set_number('2')
        self.assertEqual(self.course_class.number, '2')

        course = self.course_class.get_model_instance()

        self.assertEqual(course.number, '2')

    def test_get_name_default(self):
        self.assertEqual(self.course_class.get_name(), 'Course')

    def test_set_name_default(self):
        self.course_class.set_name('Test')
        self.assertEqual(self.course_class.name, 'Test')

        course = self.course_class.get_model_instance()
        self.assertEqual(course.name, 'Test')

    def test_get_instructor_default(self):
        self.assertEqual(self.course_class.get_instructor(), self.instructor)

    def test_set_instructor_default(self):
        instructor = InstructorClass(username='test', email='test@uwm.edu',
                                     first_name='Test', last_name='Instructor')
        instructor.save_details()
        instructor = instructor.get_model_instance()

        self.course_class.set_instructor(instructor)
        self.assertEqual(self.course_class.instructor, instructor)

        course = self.course_class.get_model_instance()
        self.assertEqual(course.instructor, instructor)

    def test_set_instructor_none(self):
        self.course_class.set_instructor(None)
        self.assertEqual(self.course_class.instructor, None)

        course = self.course_class.get_model_instance()
        self.assertEqual(course.instructor, None)

    def test_set_instructor_instructor_does_not_exist(self):
        invalid_instructor = InstructorClass(
            username='test', email='test@uwm.edu', first_name='Test', last_name='Test')

        with self.assertRaises(User.DoesNotExist, msg='set_instructor does not raise User.DoesNotExist for non-existant instructor'):
            self.invalid_class.set_instructor(
                invalid_instructor.get_model_instance())

    def test_get_tas_default(self):
        course = self.course_class.get_model_instance()
        course.user_set.add(self.ta)

        self.assertEqual(list(self.course_class.get_tas()), [self.ta])
    
    def test_get_sections(self):
        course = self.course_class.get_model_instance()
        self.assertEqual(list(self.course_class.get_sections()), [])
