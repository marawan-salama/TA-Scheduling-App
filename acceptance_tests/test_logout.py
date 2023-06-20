from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class LogoutViewTest(TestCase):
    def setUp(self):
        # Create a user and log in
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_logout_view(self):
        # Access the logout view using the client
        response = self.client.get(reverse('logout'))

        # Assert that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the user is no longer authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # Assert that the user is redirected to the desired URL (e.g., home page)
        self.assertRedirects(response, reverse('home'))
