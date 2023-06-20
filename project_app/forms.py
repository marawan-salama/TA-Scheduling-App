from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.forms import ValidationError

from project_app.models import Course, Section, User, Role

from classes.course_class import CourseClass
from classes.section_class import SectionClass
from classes.user_class import UserClass


class CreateCourseForm(forms.Form):
    subject = forms.CharField(max_length=7)
    number = forms.CharField(max_length=3)
    name = forms.CharField(max_length=100, required=False)
    instructor = forms.ModelChoiceField(queryset=User.objects.filter(role=Role.INSTRUCTOR), required=False)
    # tas = forms.ModelMultipleChoiceField(queryset=User.objects.filter(role=Role.TA), required=False)

    def clean(self):
        cleaned_data = super().clean()

        subject = cleaned_data.get('subject')
        number = cleaned_data.get('number')
        name = cleaned_data.get('name')
        instructor = cleaned_data.get('instructor')
        # tas = cleaned_data.get('tas')

        if not subject:
            raise ValidationError('Subject is empty.', code='subject')

        if not subject.isupper():
            raise ValidationError('Subject is not upper case.')

        if not number:
            raise ValidationError('Number is empty.', code='number')

        if not number.isnumeric():
            raise ValidationError('Number is not a number.')

        if instructor and instructor.role != Role.INSTRUCTOR:
            raise ValidationError('Selected "instructor" is not an instructor.')

        if instructor and instructor.role != Role.INSTRUCTOR:
            raise ValidationError('Selected "instructor" is not an instructor.')

        try:
            course = Course.objects.get(subject=subject, number=number)
            raise ValidationError(f'{course} already exists.')
        except Course.DoesNotExist:
            return cleaned_data


class EditCourseForm(forms.Form):
    subject = forms.CharField(max_length=7, required=False)
    number = forms.CharField(max_length=3, required=False)
    name = forms.CharField(max_length=100, required=False)
    instructor = forms.ModelChoiceField(queryset=User.objects.filter(role=Role.INSTRUCTOR), required=False)

    def clean(self):
        cleaned_data = super().clean()

        subject = cleaned_data.get('subject')
        number = cleaned_data.get('number')
        name = cleaned_data.get('name')
        instructor = cleaned_data.get('instructor')
        
        if not subject:
            raise ValidationError('Subject is empty.', code='subject')

        if not subject.isupper():
            raise ValidationError('Must provide a username')

        if not number:
            raise ValidationError('Number is empty.', code='number') 

        if not number.isnumeric():
            raise ValidationError('Number is not a number.')
        
        if instructor and instructor.role != Role.INSTRUCTOR:
            raise ValidationError('Selected "instructor" is not an instructor.')

        return cleaned_data


class CreateSectionForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), disabled=True)
    number = forms.CharField(max_length=3)
    ta = forms.ModelChoiceField(queryset=User.objects.filter(role=Role.TA), required=False)

    def clean(self):
        cleaned_data = super().clean()
        print('in create section')
        course = cleaned_data.get('course')
        number = cleaned_data.get('number')
        ta = cleaned_data.get('ta')

        if not number:
            raise ValidationError('Number is empty.', code='number')

        if ta and ta.role != Role.TA:
            raise ValidationError('Selected "instructor" is not an instructor.')

        try:
            print('testing if exists')
            section = Section.objects.get(number=number, course=course)
            raise ValidationError(f'{section} already exists.')
        except Section.DoesNotExist:
            return cleaned_data


class EditSectionForm(forms.Form):
    number = forms.CharField(max_length=3)
    ta = forms.ModelChoiceField(queryset=User.objects.filter(role=Role.TA), required=False)

    def clean(self):
        cleaned_data = super().clean()

        number = cleaned_data.get('number')
        ta = cleaned_data.get('ta')
        course = cleaned_data.get('course')

        if not number:
            raise ValidationError('Number is empty.', code='number')

        if ta and ta.role != Role.TA:
            raise ValidationError('Selected "instructor" is not an instructor.')

        return cleaned_data


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=150)
    last_name = forms.CharField(required=True, max_length=150)
    role = forms.IntegerField(widget=forms.Select(choices=Role.choices), initial=Role.TA, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
        exclude = ('first_name', 'last_name', 'phone_number', 'home_address')

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        role = cleaned_data.get('role')

        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()

        user_class = UserClass(username, email, first_name, last_name, role)
        user_class.validate()

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        user_class = UserClass.get_instance(user)
        user_class.set_email(self.cleaned_data.get('email'))
        user_class.set_role(self.cleaned_data('role'))

        return user_class.get_model_instance()


class EditUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    role = forms.IntegerField(widget=forms.Select(choices=Role.choices))

    def clean(self):
        pass


class ResetUserPasswordForm(forms.Form):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        max_length=128, label='Confirm Password', widget=forms.PasswordInput())
    
    def clean(self):
        pass


class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    home_address = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            self.fields['home_address'].initial = self.user.home_address
            self.fields['phone_number'].initial = self.user.phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email == self.user.email:
            return email

        if User.objects.filter(email=email).exclude(username=self.user.username).exists():
            raise forms.ValidationError('This email is already in use.')

        return email

    def save(self):
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        self.user.home_address = self.cleaned_data['home_address']
        self.user.phone_number = self.cleaned_data['phone_number']
        self.user.save()


class ChangePasswordForm(PasswordChangeForm):
    def clean(self):
        cleaned_data = super().clean()

        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise ValidationError('New passwords do not match')

        return cleaned_data