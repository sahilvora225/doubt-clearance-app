from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import Doubt
from .serializers import DoubtSerializer


DOUBT_URL = reverse('doubts:doubt-list')


def sample_user(email='test@test.com', password='test123', account_type='student'):
    return get_user_model().objects.create_user(email=email, password=password, account_type=account_type)


class DoubtModelTest(TestCase):

    def test_create_doubt_successful(self):
        user = sample_user()
        payload = {'question': 'What is the solution?',
                   'question_type': 'Maths', 'user': user}
        doubt = Doubt.objects.create(**payload)

        self.assertEqual(doubt.question, payload['question'])
        self.assertEqual(doubt.question_type, payload['question_type'])


class PublicDoubtApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_upload_doubt_user_not_authenticated(self):
        payload = {'question': 'What is the solution?',
                   'question_type': 'Maths'}
        res = self.client.post(DOUBT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDoubtApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_upload_doubt_successful(self):
        payload = {'question': 'What is the solution?',
                   'question_type': 'Maths'}
        res = self.client.post(DOUBT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Doubt.objects.filter(
            user=self.user, question_type=payload['question_type']).exists()
        self.assertTrue(exists)

    def test_upload_doubt_invalid(self):
        payload = {'question': '', 'question_type': ''}
        res = self.client.post(DOUBT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_doubts_student(self):
        res = self.client.get(DOUBT_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_doubts_teacher(self):
        payload = {'question': 'What is the solution?',
                   'question_type': 'Maths'}
        self.client.post(DOUBT_URL, payload)
        user = sample_user(email='test1@test.com', account_type='teacher')
        self.client.force_authenticate(user)
        res = self.client.get(DOUBT_URL)

        doubts = Doubt.objects.all().order_by('-question_type')
        serializer = DoubtSerializer(doubts, many=True)

        self.assertEqual(res.data, serializer.data)
