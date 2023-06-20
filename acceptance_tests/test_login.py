from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.dashboard_url = reverse('view_courses')
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(self.username, password=self.password)

    def test_login(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertRedirects(response, self.dashboard_url, status_code=302, target_status_code=200)
        self.assertTrue(authenticate(username=self.username, password=self.password))
