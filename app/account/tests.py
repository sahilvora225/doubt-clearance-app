from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


USER_CREATE_URL = reverse('account:create')
TOKEN_URL = reverse('account:token')


def sample_user_payload(email='test@test.com', password='test123', account_type='student'):
    return {'email': email, 'password': password, 'account_type': account_type}


class UserModelTest(TestCase):

    def test_create_user_successful(self):
        """Test to create a user successfully"""
        payload = {'email': 'test@test.com', 'password': 'test123', 'account_type': 'student'}
        user = get_user_model().objects.create_user(**payload)

        self.assertEqual(user.email, payload['email'])
        self.assertEqual(user.account_type, payload['account_type'])
        self.assertTrue(user.check_password(payload['password']))

    def test_create_user_normalize_email(self):
        """Test to create user along with normalizing email"""
        payload = {'email': 'test@TEST.COM', 'password': 'test123', 'account_type': 'student'}
        user = get_user_model().objects.create_user(**payload)

        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password(payload['password']))


class UserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_successful(self):
        """Test to create user successfully through API call"""
        payload = sample_user_payload()
        res = self.client.post(USER_CREATE_URL, payload)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', res.data)
        self.assertEqual(user.email, payload['email'])
        self.assertEqual(user.account_type, payload['account_type'])
        self.assertTrue(user.check_password(payload['password']))

    def test_create_user_empty_email(self):
        """Test to get error if email field is invalid"""
        payload = sample_user_payload(email='')
        res = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('account_type', res.data)

    def test_create_user_empty_account_type(self):
        """Test to get error if account type field is invalid"""
        payload = sample_user_payload(account_type='')
        res = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('email', res.data)

    def test_create_user_get_request(self):
        """Test to get error on sending GET request to create user URL"""
        res = self.client.get(USER_CREATE_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TokenApiTest(TestCase):

    def setUp(self):
        self.payload = sample_user_payload()
        self.client = APIClient()
        self.user = self.client.post(USER_CREATE_URL, self.payload)

    def test_create_token_successful(self):
        """Test to create for an authenticated user successfully"""
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """Test to get error on passing invalid credentials"""
        payload = sample_user_payload(password='test1234')
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
