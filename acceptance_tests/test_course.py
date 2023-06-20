from django.test import TestCase
from django.db.utils import IntegrityError
from project_app.models import Course, User, Role
from classes.course_class import CourseClass


class CourseAcceptanceTestSuite(TestCase):
    def setUp(self):
        self.instructor = User(username='instructor', email='instructor@uwm.edu',
                               first_name='Test', last_name='Instructor')
        self.instructor.set_password('instructor')
        self.instructor.role = Role.INSTRUCTOR
        self.instructor.save()

        self.ta = User(username='ta', email='ta@uwm.edu',
                       first_name='Test', last_name='TA')
        self.ta.set_password('ta')
        self.ta.role = Role.TA
        self.ta.save()

        self.course_class = CourseClass('COURSE', '1', 'Course', self.instructor)
        self.course_class.save_details()

        self.invalid_class = CourseClass('INVALID', '1')

    def test_save_details(self):
        # Ensure course details are saved correctly
        course = Course.objects.get(subject=self.course_class.subject, number=self.course_class.number)
        self.assertEqual(self.course_class.subject, course.subject)
        self.assertEqual(self.course_class.number, course.number)
        self.assertEqual(self.course_class.name, course.name)
        self.assertEqual(self.course_class.instructor, course.instructor)

    def test_save_details_duplicate(self):
        # Ensure saving duplicate course details raises IntegrityError
        with self.assertRaises(IntegrityError):
            self.course_class.save_details()

    def test_delete(self):
        # Ensure course is deleted successfully
        self.course_class.delete()
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(subject=self.course_class.subject, number=self.course_class.number)

    def test_delete_nonexistent(self):
        # Ensure deleting a non-existent course does not raise an error
        self.course_class.delete()
        with self.assertRaises(Course.DoesNotExist):
            self.course_class.delete()

    def test_set_subject(self):
        # Ensure subject is updated successfully
        self.course_class.set_subject('TEST')
        self.assertEqual(self.course_class.subject, 'TEST')
        course = Course.objects.get(subject=self.course_class.subject, number=self.course_class.number)
        self.assertEqual(course.subject, 'TEST')

    def test_set_subject_nonexistent(self):
        # Ensure setting subject for a non-existent course raises Course.DoesNotExist
        with self.assertRaises(Course.DoesNotExist):
            self.invalid_class.set_subject('Test')
