from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from user.models import User
from user.serializers import UserSignUpSerializer


class UserViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Add the correct URL name for registration
        self.registration_url = reverse('user-registration')
        self.login_url = reverse('login')  # Add the correct URL name for login
        # Add the correct URL name for logout
        self.logout_url = reverse('logout')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        response = self.client.post(
            self.registration_url, data=self.user_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Including the user created in setUp
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(
            self.login_url, data=login_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertIn('user', response.data)

    def test_user_login_invalid_credentials(self):
        login_data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        response = self.client.post(
            self.login_url, data=login_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'],
                         'Invalid Email or password!!')

    def test_user_logout(self):
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(
            self.login_url, data=login_data, content_type='application/json')
        refresh_token = login_response.cookies.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']).value
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
                            ] = refresh_token
        logout_response = self.client.post(
            self.logout_url, content_type='application/json')
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

    def test_user_logout_invalid_token(self):
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
                            ] = 'invalidtoken'
        response = self.client.post(
            self.logout_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid Token')
