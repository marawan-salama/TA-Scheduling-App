from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Role(models.IntegerChoices):
    SUPERVISOR = 1, _('Supervisor')
    INSTRUCTOR = 2, _('Instructor')
    TA = 3, _('TA')


class User(AbstractUser):
    role = models.PositiveSmallIntegerField(
        choices=Role.choices, blank=True, null=True)
    home_address = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(
        max_length=10, blank=True, null=True, unique=True)

    courses = models.ManyToManyField('project_app.Course', blank=True)

    # section_set: A list of sections the user is assigned to
    # sent_notifications: A list of notifications the user has sent
    # received_notifications: A list of notifications sent to the user

    class Meta:
        ordering = ['role', 'first_name', 'last_name']

    def is_supervisor(self):
        return self.role == Role.SUPERVISOR

    def is_instructor(self):
        return self.role == Role.INSTRUCTOR

    def is_ta(self):
        return self.role == Role.TA

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Course(models.Model):
    name = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=7)
    number = models.CharField(max_length=3, unique=True)

    instructor = models.ForeignKey('project_app.User', on_delete=models.SET_NULL,
                                   blank=True, null=True, limit_choices_to={'role': Role.INSTRUCTOR})

    # user_set: List of users in the course
    # section_set: List of sections in the course

    class Meta:
        ordering = ['subject', 'number']

    def __str__(self):
        return f'{self.subject} {self.number}'


class Section(models.Model):
    number = models.CharField(max_length=3)
    course = models.ForeignKey('project_app.Course', on_delete=models.CASCADE)
    ta = models.ForeignKey('project_app.User', on_delete=models.SET_NULL,
                           blank=True, null=True, limit_choices_to={'role': Role.TA})

    class Meta:
        ordering = ['course__subject', 'course__number', 'number']

    def __str__(self):
        return f'{self.course.subject} {self.course.number} - {self.number}'


class Notification(models.Model):
    sender = models.ForeignKey(
        'project_app.User', on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(
        'project_app.User', on_delete=models.CASCADE, related_name='received_notifications')
    subject = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        ordering = ['sender__last_name', 'sender__first_name']

    def __str__(self):
        return f' {self.sender} -> {self.recipient}'
