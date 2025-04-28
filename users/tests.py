from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser  # adjust if needed

class RegisterViewTests(TestCase):
    
    def test_register_valid_user(self):
        form_data = {
            'username': 'test',
            'email': 'test@test.tests',
            'phone_number': '123456789',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }
        response = self.client.post(reverse('users:register'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(email='test@test.tests').exists())

    def test_register_passwords_do_not_match(self):
        form_data = {
            'username': 'test1',
            'email': 'test1@test.test',
            'phone_number': '123456789',
            'password1': 'StrongPassword123',
            'password2': 'WrongPassword123',
        }
        response = self.client.post(reverse('users:register'), data=form_data)

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('password2'))
        self.assertIn("The two password fields didn’t match.", form.errors['password2'])

    def test_register_common_password(self):
        form_data = {
            'username': 'test2',
            'email': 'test2@test.test',
            'phone_number': '123456789',
            'password1': 'password123',
            'password2': 'password123',
        }
        response = self.client.post(reverse('users:register'), data=form_data)

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('password2'))
        self.assertIn("This password is too common.", form.errors['password2'])