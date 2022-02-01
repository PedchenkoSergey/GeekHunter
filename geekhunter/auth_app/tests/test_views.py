from django.test import TestCase
from django.test.client import Client

from auth_app.models import PortalUser


class AuthAppTestCase(TestCase):
    new_employee_user_data = {
        'email': 'employee@geekhunter.com',
        'username': 'employee',
        'first_name': 'test',
        'last_name': 'employee',
        'phone': '123',
        'password1': 'testPassword1',
        'password2': 'testPassword1',
        'roles': 'EMPLOYEE',
    }
    new_company_user_data = {
        'email': 'company@geekhunter.com',
        'username': 'company',
        'first_name': 'test',
        'last_name': 'company',
        'phone': '321',
        'password1': 'testPassword2',
        'password2': 'testPassword2',
        'roles': 'COMPANY',
    }

    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'email': 'testuser@geekhunter.com',
            'phone': '234',
            'password': 'password',
        }
        self.superuser_credentials = {
            'username': 'admin',
            'email': 'admin@geekhunter.com',
            'phone': '432',
            'password': 'password',
            'is_active': True,
            'is_superuser': True,
            'is_staff': True,
        }
        self.user = PortalUser.objects.create_user(**self.user_credentials)
        self.superuser = PortalUser.objects.create_superuser(**self.superuser_credentials)

        self.client = Client()

    def is_anonymous(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['user'].is_anonymous)

    def is_authenticated(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['user'].is_authenticated)

    def user_login(self, username, password):
        self.is_anonymous()
        response = self.client.post(
            '/auth/login/',
            data={
                'username': username,
                'password': password,
            }
        )
        self.assertEqual(302, response.status_code)

    def user_logout(self):
        self.client.get('/auth/logout/')

    def test_user_flow(self):
        self.user_login(
            username=self.user.username,
            password=self.user_credentials['password']
        )
        self.is_authenticated()
        self.user_logout()
        self.is_anonymous()

    def test_login_page_anonymous_user_ok(self):
        self.is_anonymous()
        response = self.client.get('/auth/login/')
        self.assertEqual(200, response.status_code)

    def test_signup_page_anonymous_user_ok(self):
        self.is_anonymous()
        response = self.client.get('/auth/signup/')
        self.assertEqual(200, response.status_code)

    def test_login_page_authenticated_user_redirect(self):
        self.user_login(
            username=self.user.username,
            password=self.user_credentials['password']
        )
        response = self.client.get('/auth/login/')
        self.assertEqual(302, response.status_code)

    def test_signup_page_authenticated_user_redirect(self):
        self.user_login(
            username=self.user.username,
            password=self.user_credentials['password']
        )
        response = self.client.get('/auth/signup/')
        self.assertEqual(302, response.status_code)

    def register_start(self):
        self.is_anonymous()
        response = self.client.get('/auth/signup/')
        self.assertEqual(200, response.status_code)

    def test_user_employee_register(self):
        self.register_start()
        response = self.client.post(
            '/auth/signup/',
            data=self.new_employee_user_data,
        )
        self.assertEqual(302, response.status_code)
        new_user = PortalUser.objects.get(username=self.new_employee_user_data['username'])
        self.assertTrue(new_user.is_active)
        self.assertTrue(new_user.is_employee)
        self.assertFalse(new_user.is_company)

    def test_user_company_register(self):
        self.register_start()
        response = self.client.post(
            '/auth/signup/',
            data=self.new_company_user_data,
        )
        self.assertEqual(302, response.status_code)
        new_user = PortalUser.objects.get(username=self.new_company_user_data['username'])
        self.assertTrue(new_user.is_active)
        self.assertFalse(new_user.is_employee)
        self.assertTrue(new_user.is_company)

