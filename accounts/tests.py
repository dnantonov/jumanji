from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='user_test',
            first_name='Test',
            last_name='Test',
            password='test_password',
        )

    def test_register_user(self):
        url = reverse('register')
        response = self.client.post(url, data=dict(username='test', first_name='Test', last_name='Test',
                                                   password1='test_password', password2='test_password'))
        self.assertEqual(302, response.status_code)

    def test_login_user(self):
        url = reverse('login')
        response = self.client.post(url, data=dict(username='user_test', password='test_password'))
        self.assertEqual(200, response.status_code)

    def test_logout_user(self):
        login_url = reverse('login')
        login_response = self.client.post(login_url, data=dict(username='user_test', password='test_password'))
        self.assertEqual(200, login_response.status_code)
        logout_url = reverse('logout')
        logout_response = self.client.get(logout_url)
        self.assertEqual(302, logout_response.status_code)

