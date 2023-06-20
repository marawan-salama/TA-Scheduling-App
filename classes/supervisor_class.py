from django.core.exceptions import ValidationError

from project_app.models import Course, Section, Role

from .course_class import CourseClass
from .section_class import SectionClass
from .user_class import UserClass
from .instructor_class import InstructorClass
from .ta_class import TAClass
from .notification_class import NotificationClass


class SupervisorClass(InstructorClass):
    def __init__(self, username, email, first_name, last_name, phone_number=None, home_address=None,
                 sent_notifications=[], received_notifications=[]):
        super().__init__(username, email, first_name, last_name, phone_number,
                         home_address, [], sent_notifications, received_notifications)
        self.role = Role.SUPERVISOR

    @classmethod
    def get_instance(cls, supervisor):
        return cls(
            supervisor.username,
            supervisor.email,
            supervisor.first_name,
            supervisor.last_name,
            supervisor.phone_number,
            supervisor.home_address,
            list(supervisor.sent_notifications.all()),
            list(supervisor.received_notifications.all())
        )

    def validate(self):
        super().validate()

        if self.role is not Role.SUPERVISOR:
            raise ValidationError('Role is not supervisor.')

    def get_courses(self):
        return Course.objects.all()

    def has_course(self, course):
        return Course.objects.filter(subject=course.subject, number=course.number).exists()

    def add_course(self, course):
        pass

    def get_sections(self):
        return Section.objects.all()

    def has_section(self, section):
        return Section.objects.filter(course=section.course, number=section.number).exists()

    def create_user(self, username, email, password, first_name, last_name, role=Role.TA, phone_number=None, home_address=None, courses=[], sent_notifications=[], received_notifications=[]):
        user_class = UserClass(username, email, first_name, last_name, role, phone_number,
                         home_address, courses, sent_notifications, received_notifications)
        user_class.save_details()
        user_class.set_password(password)

        return user_class.get_model_instance()

    def delete_user(self, user):
        user_class = UserClass.get_instance(user)
        user_class.delete()

    def edit_user(self, user, username, email, password, first_name, last_name, role=Role.TA, phone_number=None, home_address=None):
        user_class = UserClass.get_instance(user)

        user_class.set_username(username)
        user_class.set_email(email)
        user_class.set_first_name(first_name)
        user_class.set_last_name(last_name)
        user_class.set_password(password)
        user_class.set_role(role)
        user_class.set_phone_number(phone_number)
        user_class.set_home_address(home_address)

        return user_class.get_model_instance()

    def create_course(self, subject, number, name='', instructor=None):
        course_class = CourseClass(subject, number, name, instructor)
        course_class.save_details()

        return course_class.get_model_instance()

    def delete_course(self, course):
        course_class = CourseClass.get_instance(course)
        course_class.delete()

    def edit_course(self, course, subject, number, name, instructor=None):
        course_class = CourseClass.get_instance(course)

        course_class.set_subject(subject)
        course_class.set_number(number)
        course_class.set_name(name)
        course_class.set_instructor(instructor)

        return course_class.get_model_instance()

    def create_section(self, course, number, tas=[]):
        section_class = SectionClass(number, course, tas)
        section_class.save_details()

        return section_class.get_model_instance()

    def delete_section(self, section):
        section_class = SectionClass.get_instance(section)
        section_class.delete()

    def assign_instructor_course(self, instructor, course):
        instructor_class = InstructorClass.get_instance(instructor)
        course_class = CourseClass.get_instance(course)
        
        instructor_class.add_course(course)
        course_class.set_instructor(instructor)
        
        course = course.refresh_from_db()

    def assign_ta_course(self, ta, course):
        ta_class = TAClass.get_instance(ta)
        ta_class.add_course(course)
    
    def remove_ta_course(self, ta, course):
        pass
    
    def send_notifications(self, subject, message):
        notifications = []
        supervisor = self.get_model_instance()

        for user in UserClass.all().exclude(username=supervisor.username):
            notification_class = NotificationClass(supervisor, user, subject, message)
            notification_class.save_details()
            notifications.append(notification_class.get_model_instance())

        return notifications
