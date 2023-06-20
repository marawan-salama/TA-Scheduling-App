from project_app.models import Section
from .ta_class import TAClass

class SectionClass:
    def __init__(self, number, course, ta=None):
        self.number = number
        self.course = course
        self.ta = ta

    @classmethod
    def get_instance(cls, section):
        return cls(
            section.number,
            section.course,
            section.ta
        )

    def save_details(self):
        section = Section(number=self.number, course=self.course)
        section.save()

        if self.ta:
            section.tas.add(self.ta.get_model_instance())  # Add the TA to the 'tas' many-to-many relationship
            section.save()

        return f'Added {self.course.subject} {self.course.number} - {self.number} to the system.'

    def get_model_instance(self):
        return Section.objects.get(course=self.course, number=self.number)

    def validate(self):
        pass

    def delete(self):
        section = self.get_model_instance()
        section.delete()

    def get_number(self):
        return self.number

    def set_number(self, number):
        section = self.get_model_instance()
        section.number = number
        section.save()

        self.number = number

    def get_course(self):
        return self.course

    def set_ta(self, ta):
        user = ta.get_model_instance()  # Assuming get_model_instance() returns a User instance
        section = self.get_model_instance()
        section.tas.add(user)  # Add the TA to the 'tas' many-to-many relationship
        section.save()
