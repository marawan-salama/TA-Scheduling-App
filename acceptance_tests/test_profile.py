from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ProfileViewTest(TestCase):
    def setUp(self):
        # Create a user and log in
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_profile_view(self):
        # Access the profile view using the client
        response = self.client.get(reverse('profile'))

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
