from django.core.exceptions import ValidationError

from project_app.models import Role

from .ta_class import TAClass
from .course_class import CourseClass
from .section_class import SectionClass
from .notification_class import NotificationClass


class InstructorClass(TAClass):
    def __init__(self, username, email, first_name, last_name, phone_number=None, home_address=None, courses=[],
                 sent_notifications=[], received_notifications=[]):
        super().__init__(username, email, first_name, last_name, phone_number, home_address, courses,
                         received_notifications)
        self.role = Role.INSTRUCTOR
        self.sent_notifications = sent_notifications

    @classmethod
    def get_instance(cls, instructor):
        return cls(
            instructor.username,
            instructor.email,
            instructor.first_name,
            instructor.last_name,
            instructor.phone_number,
            instructor.home_address,
            list(instructor.courses.all()),
            list(instructor.sent_notifications.all()),
            list(instructor.received_notifications.all())
        )

    def validate(self):
        super().validate()

        if self.role is not Role.INSTRUCTOR:
            raise ValidationError('Role is not instructor.')

    def assign_ta_section(self, ta, section):
        section_class = SectionClass.get_instance(section)
        section_class.set_ta(ta)

    def remove_ta_section(self, ta, section):
        pass

    def get_sent_notifications(self):
        return self.sent_notifications

    def send_notifications(self, course, subject, message):
        notifications = []
        instructor = self.get_model_instance()
        course_class = CourseClass.get_instance(course)

        for ta in course_class.get_tas():
            notification_class = NotificationClass(instructor, ta, subject, message)
            notification_class.save_details()
            notifications.append(notification_class.get_model_instance())

        return notifications