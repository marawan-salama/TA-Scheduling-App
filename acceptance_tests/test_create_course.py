from django.test import TestCase
from project_app.models import Course


class CreateCourseAcceptanceTest(TestCase):
    def test_create_course(self):
        # Define the course details
        subject = 'COURSE1'
        number = '101'
        name = 'Course 1'

        # Create the course
        course = Course(subject=subject, number=number, name=name)
        course.save()

        # Retrieve the created course from the database
        created_course = Course.objects.get(subject=subject, number=number)

        # Verify that the created course has the correct details
        self.assertEqual(created_course.subject, subject)
        self.assertEqual(created_course.number, number)
        self.assertEqual(created_course.name, name)
