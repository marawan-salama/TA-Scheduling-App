from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from project_app.models import Course, Section, User, Role
from project_app.forms import CreateCourseForm, EditCourseForm, CreateSectionForm, EditSectionForm, CreateUserForm, \
    EditUserForm, UpdateProfileForm, ChangePasswordForm

from classes.course_class import CourseClass
from classes.section_class import SectionClass
from classes.supervisor_class import SupervisorClass
from classes.instructor_class import InstructorClass
from classes.user_class import UserClass


# Create your views here.
class Profile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'main/profile.html')


class ViewCourses(LoginRequiredMixin, View):
    def get(self, request):
        user_class = UserClass.get_instance(request.user)
        courses = user_class.get_courses()

        return render(request, 'main/courses.html', {'courses': courses})


class ViewCourse(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        course_class = CourseClass.get_instance(course)
        user_class = UserClass.get_instance(request.user)

        if not user_class.has_course(course):
            return redirect('/courses/')

        return render(request, 'main/course.html', {'course': course, 'tas': course_class.get_tas(),
                                                    'sections': course_class.get_sections()})


class CreateCourse(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_supervisor():
            return redirect('/courses/')

        form = CreateCourseForm()

        return render(request, 'main/create_course.html', {'form': form})

    def post(self, request):
        form = CreateCourseForm(request.POST)
        message = ''

        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            number = form.cleaned_data.get('number')
            name = form.cleaned_data.get('name')
            instructor = form.cleaned_data.get('instructor')

            course_class = CourseClass(subject, number, name, instructor)
            message = course_class.save_details()

        return render(request, 'main/create_course.html', {'form': form, 'message': message})


class DeleteCourse(LoginRequiredMixin, View):
    def get(self, request, course_id):
        # Only allow supervisors to delete a course
        if not request.user.is_supervisor():
            return redirect('/courses/')

        course = get_object_or_404(Course, pk=course_id)
        return render(request, 'main/delete_course.html', {'course': course})

    def post(self, request, course_id):
        # Only allow supervisors to delete a course
        if not request.user.is_supervisor():
            return redirect('/courses/')

        course = get_object_or_404(Course, pk=course_id)
        course.delete()
        return redirect('/courses/')


class EditCourse(LoginRequiredMixin, View):
    def get(self, request, course_id):
        if not request.user.is_supervisor():
            return redirect(f'/course/{course_id}')

        course = get_object_or_404(Course, pk=course_id)
        course_class = CourseClass.get_instance(course)

        form = EditCourseForm(
            initial={
                'subject': course_class.get_subject(),
                'number': course_class.get_number(),
                'name': course_class.get_name(),
                'instructor': course_class.get_instructor()
            }
        )

        return render(request, 'main/edit_course.html', {'course': course, 'form': form})

    def post(self, request, course_id):
        if not request.user.is_supervisor():
            return redirect(f'/course/{course_id}')

        course = get_object_or_404(Course, pk=course_id)
        course_class = CourseClass.get_instance(course)

        form = EditCourseForm(
            request.POST,
            initial={
                'subject': course_class.get_subject(),
                'number': course_class.get_number(),
                'name': course_class.get_name(),
                'instructor': course_class.get_instructor()
            }
        )

        message = ''

        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            number = form.cleaned_data.get('number')
            name = form.cleaned_data.get('name')
            instructor = form.cleaned_data.get('instructor')

            course_class.set_subject(subject)
            course_class.set_number(number)
            course_class.set_name(name)
            course_class.set_instructor(instructor)

            course = get_object_or_404(Course, subject=subject, number=number)

            message = f'Successfully updated {subject} {number}.'

        return render(request, 'main/edit_course.html', {'course': course, 'form': form, 'message': message})


class CreateSection(LoginRequiredMixin, View):
    def get(self, request, course_id):
        if not request.user.is_supervisor():
            return redirect(f'/course/{course_id}/')

        course = get_object_or_404(Course, pk=course_id)
        form = CreateSectionForm(
            initial={
                'course': course,
                'number': 000
            }
        )

        return render(request, 'main/create_section.html', {'course_id': course_id, 'form': form})

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        form = CreateSectionForm(
            request.POST,
            initial={
                'course': course
            }
        )
        message = ''

        if form.is_valid():
            number = form.cleaned_data.get('number')
            ta = form.cleaned_data.get('ta')
            course = form.cleaned_data.get('course')

            section_class = SectionClass(number, course, ta)
            message = section_class.save_details()

        return render(request, 'main/create_section.html', {'course_id': course_id, 'form': form, 'message': message})


class DeleteSection(LoginRequiredMixin, View):
    def get(self, request, course_id, section_id):
        # Only allow supervisors to delete a section
        if not request.user.is_supervisor():
            return redirect('/courses/')

        section = get_object_or_404(Section, pk=section_id)
        course = get_object_or_404(Course, pk=course_id)
        return render(request, 'main/delete_section.html', {'course': course, 'section': section})

    def post(self, request, course_id, section_id):
        # Only allow supervisors to delete a section
        if not request.user.is_supervisor():
            return redirect('/courses/')

        section = get_object_or_404(Section, pk=section_id)
        section.delete()
        return redirect(f'/courses/{course_id}/')


class EditSection(LoginRequiredMixin, View):
    def get(self, request, course_id, section_id):
        if not request.user.is_supervisor():
            return redirect(f'/courses/{course_id}')

        section = get_object_or_404(Section, pk=section_id)
        section_class = SectionClass.get_instance(section)
        course = get_object_or_404(Course, pk=course_id)

        form = EditSectionForm(
            initial={
                'number': section.number,
                'ta': section.ta
            }
        )

        return render(request, 'main/edit_section.html', {'course': course, 'section': section, 'form': form})

    def post(self, request, course_id, section_id):
        if not request.user.is_supervisor():
            return redirect(f'/course/{course_id}')

        section = get_object_or_404(Section, pk=section_id)
        section_class = SectionClass.get_instance(section)
        course = get_object_or_404(Course, pk=course_id)

        form = EditSectionForm(
            request.POST,
            initial={
                'number': section_class.get_number(),
                'ta': section.ta,
                'course': course
            }
        )

        message = ''

        if form.is_valid():
            number = form.cleaned_data.get('number')
            ta = form.cleaned_data.get('ta')

            section_class.set_number(number)
            section_class.set_ta(ta)

            section = get_object_or_404(Section, number=number, course=course_id)

            message = f'Successfully updated {course.subject} {course.number} - {section.number}.'

        return render(request, 'main/edit_section.html', {'course': course, 'section': section, 'form': form,
                                                          'message': message})


class ViewUsers(LoginRequiredMixin, View):
    def get(self, request):
        users = UserClass.all().exclude(username='admin')

        if not request.user.is_supervisor():
            return redirect('/courses/')

        return render(request, 'main/users.html', {'users': users})


class ViewUser(LoginRequiredMixin, View):
    def get(self, request, user_id):
        requested_user = get_object_or_404(User, pk=user_id)

        return render(request, 'main/user.html', {'requested_user': requested_user})


class CreateUser(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_supervisor():
            return redirect('/users/')

        form = CreateUserForm()

        return render(request, 'main/create_user.html', {'form': form})

    def post(self, request):
        if not request.user.is_supervisor():
            return redirect('/users/')

        supervisor_class = SupervisorClass.get_instance(request.user)
        form = CreateUserForm(request.POST)
        message = ''

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            role = form.cleaned_data.get('role')

            supervisor_class.create_user(username, email, password, first_name, last_name, role)
            message = f'Successfully created {first_name} {last_name}.'

        return render(request, 'main/create_user.html', {'form': form, 'message': message})


class DeleteUser(LoginRequiredMixin, View):
    def get(self, request, user_id):
        if not request.user.is_supervisor():
            return redirect('/users/')

        requested_user = get_object_or_404(User, pk=user_id)
        return render(request, "main/delete_user.html", {'requested_user': requested_user})

    def post(self, request, user_id):
        if not request.user.is_supervisor():
            return redirect('/users/')

        requested_user = get_object_or_404(User, pk=user_id)
        requested_user.delete()

        return redirect('/users/')


class EditUser(LoginRequiredMixin, View):
    def get(self, request, user_id):
        if not request.user.is_supervisor():
            return redirect(f'/users/{user_id}/')

        requested_user = get_object_or_404(User, pk=user_id)
        user_class = UserClass.get_instance(requested_user)

        form = EditUserForm(
            initial={
                'username': user_class.get_username(),
                'email': user_class.get_email(),
                'first_name': user_class.get_first_name(),
                'last_name': user_class.get_last_name(),
                'role': user_class.get_role()
            }
        )

        return render(request, "main/edit_user.html", {'requested_user': requested_user, 'form': form})

    def post(self, request, user_id):
        if not request.user.is_supervisor():
            return redirect(f'/users/{user_id}')

        requested_user = get_object_or_404(User, pk=user_id)
        user_class = UserClass.get_instance(requested_user)

        form = EditUserForm(
            request.POST,
            initial={
                'username': user_class.get_username(),
                'email': user_class.get_email(),
                'first_name': user_class.get_first_name(),
                'last_name': user_class.get_last_name(),
                'role': user_class.get_role()
            }
        )
        message = ''

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            role = form.cleaned_data.get('role')

            user_class.set_username(username)
            user_class.set_email(email)
            user_class.set_first_name(first_name)
            user_class.set_last_name(last_name)
            user_class.set_role(role)

            requested_user = get_object_or_404(User, pk=user_id)

            message = f'Successfully updated {requested_user}'

        return render(request, 'main/edit_user.html',
                      {'requested_user': requested_user, 'form': form, 'message': message})


class UpdateProfileView(View):
    def get(self, request):
        form = UpdateProfileForm(user=request.user)
        return render(request, 'main/update_profile.html', {'form': form})

    def post(self, request):
        form = UpdateProfileForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'main/update_profile.html', {'form': form})


class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'main/change_password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        return render(request, 'main/change_password.html', {'form': form})
