from django.db.utils import IntegrityError
from django.contrib.auth.password_validation import ValidationError, validate_password

from project_app.models import User, Role

from project.settings import AUTH_EMAIL_DOMAIN


class UserClass:
    def __init__(self, username, email, first_name, last_name, role=None, phone_number=None, home_address=None,
                 courses=[], sent_notifications=[], received_notifications=[]):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.home_address = home_address
        self.role = role
        self.courses = courses
        self.sent_notifications = sent_notifications
        self.received_notifications = received_notifications

    @classmethod
    def get_instance(cls, user):
        from .supervisor_class import SupervisorClass
        from .instructor_class import InstructorClass
        from .ta_class import TAClass

        if user.is_supervisor():
            return SupervisorClass.get_instance(user)

        if user.is_instructor():
            return InstructorClass.get_instance(user)

        if user.is_ta():
            return TAClass.get_instance(user)

        return cls(
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.role,
            user.phone_number,
            user.home_address,
            list(user.courses.all()),
            list(user.sent_notifications.all()),
            list(user.received_notifications.all())
        )

    def save_details(self):
        user = User(username=self.username, email=self.email, first_name=self.first_name,
                    last_name=self.last_name, role=self.role)
        user.role = self.role
        user.save()

        user.courses.set(self.courses)

    def get_model_instance(self):
        return User.objects.get(username=self.get_username())

    def validate(self):
        if User.objects.filter(username=self.username).exists():
            raise ValidationError('Username is taken.')

        if User.objects.filter(email=self.email).exists():
            raise ValidationError('User with that email already exists!')

        domain_length = len(AUTH_EMAIL_DOMAIN)
        if self.email[-domain_length:] != AUTH_EMAIL_DOMAIN:
            raise ValidationError(f'Email does not end with {AUTH_EMAIL_DOMAIN}')

        roles = set(role.value for role in Role)
        if self.role not in roles:
            raise ValidationError('Role does not exist!')

        if self.phone_number and not self.phone_number.isnumeric():
            raise ValidationError('Phone number can only contain digits.')

    def delete(self):
        user = self.get_model_instance()
        user.delete()

    def get_username(self):
        return self.username

    def set_username(self, username):
        user = self.get_model_instance()
        user.username = username
        user.save()

        self.username = username

    def get_email(self):
        return self.email

    def set_email(self, email):
        user = self.get_model_instance()
        user.email = email
        user.save()

        self.email = email

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        user = self.get_model_instance()
        user.first_name = first_name
        user.save()

        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        user = self.get_model_instance()
        user.last_name = last_name
        user.save()

        self.last_name = last_name

    def get_role(self):
        return self.role

    def set_role(self, role):
        user = self.get_model_instance()
        user.role = role
        user.save()

        self.role = role

    def set_password(self, raw_password):
        user = self.get_model_instance()

        validate_password(raw_password)
        user.set_password(raw_password)
        user.save()

    def set_phone_number(self, phone_number):
        user = self.get_model_instance()
        user.phone_number = phone_number
        user.save()

        self.phone_number = phone_number

    def set_home_address(self, home_address):
        user = self.get_model_instance()
        user.home_address = home_address
        user.save()

        self.home_address = home_address

    def get_courses(self):
        user = self.get_model_instance()
        return user.courses.all()

    def has_course(self, course):
        user = self.get_model_instance()
        return user.courses.filter(subject=course.subject, number=course.number).exists()

    def add_course(self, course):
        user = self.get_model_instance()

        if not self.has_course(course):
            user.courses.add(course)
            self.courses = list(user.courses.all())

    def get_received_notifications(self):
        user = self.get_model_instance()
        return user.received_notifications.all()

    def is_supervisor(self):
        return self.role == Role.SUPERVISOR

    def is_instructor(self):
        return self.role == Role.INSTRUCTOR

    def is_ta(self):
        return self.role == Role.TA

    @staticmethod
    def all():
        return User.objects.all()
