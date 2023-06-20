from django.test import TestCase
from django.contrib.auth.models import User
from project_app.models import User, Role

class UsersAcceptanceTest(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='admin', password='password')
        self.role = Role.SUPERVISOR  # Use the role enumeration choice

    def test_list_users(self):
        # Authenticate the client
        self.client.login(username='admin', password='password')

        # Create some sample users
        user1 = User.objects.create(username='user1', email='user1@example.com', password='password1', role=self.role)
        user2 = User.objects.create(username='user2', email='user2@example.com', password='password2', role=self.role)
        user3 = User.objects.create(username='user3', email='user3@example.com', password='password3', role=self.role)

        # Retrieve the list of users
        response = self.client.get('/users/', follow=True)  # Follow redirects

        # Verify the final response status code
        self.assertEqual(response.status_code, 200)

        # Verify that all the users are present in the final response
        self.assertContains(response, user1.username)
        self.assertContains(response, user2.username)
        self.assertContains(response, user3.username)
