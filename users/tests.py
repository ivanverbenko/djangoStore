from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {'first_name': 'first_name', 'last_name': 'last_name', 'username': 'username',
                     'email': 'test@mail.ru',
                     'password1': 'sdfsdafsdf!1s', 'password2': 'sdfsdafsdf!1s'}

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        response = self.client.post(self.path, self.data)
        username = self.data['username']
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # emailVerification

        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())

    def test_user_registration_post_error(self):
        username = self.data['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'You should check in on some of those fields below.')
