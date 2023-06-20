from django.test import TestCase
from django.test import Client
from project_app.models import User, Role


class TestCreateUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = User.objects.create(first_name='Supervisor', last_name='Test', email='super@uwm.edu',
                                              username="super", password="super", role=Role.SUPERVISOR)
        self.instructor = User.objects.create(first_name='Instructor', last_name='Test', email='inst@uwm.edu',
                                              username="inst", password="inst", role=Role.INSTRUCTOR)
        self.ta = User.objects.create(first_name='TA', last_name='Test', email='ta@uwm.edu', username="ta",
                                      password="ta", role=Role.TA)

    def test_ta_view(self):
        # response = self.client.post('/', {'username': self.ta.username, 'password': self.ta.password})
        # self.assertEqual(response.url, '/login/')
        #
        # response = self.client.get('/create_user/', {'username': self.ta.username})
        # self.assertRedirects(response, '/users/', status_code=404, target_status_code=200)
        pass

    def test_instructor_view(self):
        # response = self.client.post('/', {'username': self.instructor.username, 'password': self.instructor.password})
        # self.assertEqual(response.url, '/login/')
        # #
        # response = self.client.get('/create_user/', {'username': self.instructor.username})
        # self.assertRedirects(response.url, '/users/')
        pass

    def test_supervisor_view(self):
        # response = self.client.post('/', {'username': self.supervisor.username, 'password': self.supervisor.password})
        # self.assertEqual(response.url, '/login/')
        # #
        # response = self.client.get('/users/create', {'username': self.supervisor.username})
        # self.assertRedirects(response.url, 'users/')
        pass

    def test_empty_parameter(self):
        resp = self.client.post("/users/create/", {"first_name": "", "last_name": ""}, follow=True)
        form = resp.context['form']
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors, "Please fill out this section", msg='Created account with empty parameter')

    def test_invalid_username(self):
        resp = self.client.post("/users/create/", {"username": "newuser", "email": "newuser@uwm.edu",
                                                   "first_name": "New", "last_name": "User"}, follow=True)
        form = resp.context['form']
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['username'], "Must provide a username", msg='Created account with empty parameter')

    def test_invalid_email(self):
        resp = self.client.post("/users/create/", {"username": "newuser", "email": "newuser@google.com",
                                                   "first_name": "New", "last_name": "User"}, follow=True)
        form = resp.context['form']
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['email'], "Email does not end with @uwm.edu",
                         msg='Created account with invalid email')

    def test_invalid_first_name(self):
        resp = self.client.post("/users/create/", {"username": "newuser", "email": "newuser@uwm.edu",
                                                   "first_name": "new", "last_name": "User"}, follow=True)
        form = resp.context['form']
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['first_name'], "Please fill out this section",
                         msg='Created account with empty parameter')

    def test_invalid_last_name(self):
        resp = self.client.post("/users/create/", {"username": "newuser", "email": "newuser@uwm.edu",
                                                   "first_name": "New", "last_name": "user"}, follow=True)
        form = resp.context['form']
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['last_name'], "Please fill out this section",
                         msg='Created account with empty parameter')

    def test_none_matching_passwords(self):
        resp = self.client.post("/users/create/", {"username": "newuser", "email": "newuser@uwm.edu",
                                                   "first_name": "New", "last_name": "User"}, follow=True)
        form = resp.context['form']
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['last_name'], "Please fill out this section",
                         msg='Created account with empty parameter')

    def test_preexisting_username(self):
        resp = self.client.post("/users/create/", {"first_name": "New", "last_name": "User", "email": "test@uwm.edu",
                                                   "username": "super", "password": "test", "staff_role": "supervisor"},
                                follow=True)
        form = resp.context['form']
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['last_name'], "Username is taken.",
                         msg='Created account with duplicate username')

    def test_preexisiting_email(self):
        resp = self.client.post("/users/create/", {"first_name": "New", "last_name": "User", "email": "super@uwm.edu",
                                                   "username": "test", "password": "test", "staff_role": "supervisor"},
                                follow=True)
        self.assertEqual(resp.context["message"], "User with that email already exists!",
                         msg='Created account with duplicate email')

    def test_successful_user_creation(self):
        response = self.client.post('/', {'username': self.supervisor.username, 'password': self.supervisor.password})
        self.assertEqual(response.url, '/login/')

        resp = self.client.post("/users/create/", {"first_name": "New", "last_name": "User", "email": "test@uwm.edu",
                                "username": "test", "password": "test", "password": "test", "staff_role": "supervisor"},
                                follow=True)
        self.assertEqual(resp.context["message"], "'New User' has been created",
                         msg='Did not create account')
