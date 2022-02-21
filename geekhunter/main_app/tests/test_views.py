from django.core.paginator import Paginator
from django.test import TestCase
from django.test.client import Client

from auth_app.models import PortalUser
from news_app.models import News


class MainAppTestCase(TestCase):
    SUCCESS_RESPONSE_CODE = 200
    REDIRECT_RESPONSE_CODE = 302
    PERMISSON_DENIED_CODE = 403
    PAGE_NOT_FOUND_CODE = 404

    def setUp(self) -> None:
        client = Client()

        self.news_list = News.objects.get_queryset().order_by('id')
        self.paginator = Paginator(self.news_list, 2)

        self.user_credentials = {
            'username': 'testuser',
            'email': 'testuser@geekhunter.com',
            'phone': '123124',
            'password': 'password',
        }
        self.user = PortalUser.objects.create_user(**self.user_credentials)

    def test_main_page_ok(self):
        response = self.client.get('')
        self.assertEqual(200, response.status_code)

    def test_news_page_not_a_int(self):
        response = self.client.get('/?page=str')
        self.assertEqual(200, response.status_code)

    def test_news_empty_page(self):
        response = self.client.get(f'/?page={self.paginator.num_pages + 1}')
        self.assertEqual(200, response.status_code)

    def test_login_page_ok(self):
        response = self.client.get('/auth/login/')
        self.assertEqual(200, response.status_code)

    def test_view_user_profile_ok(self):
        self.client.login(username=self.user.username, password=self.user_credentials['password'])

        response = self.client.get('/user/profile/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_user_profile_update_data_with_password(self):
        self.client.login(username=self.user.username, password=self.user_credentials['password'])

        data = {
            'username': 'testuser1',
            'password': 'newpassword',
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
            'phone': '06086304638',
            'email': 'testuser@newmail.com',
        }

        response = self.client.post(
            '/user/profile/',
            data=data,
        )
        self.assertEqual(self.REDIRECT_RESPONSE_CODE, response.status_code)

        self.assertEqual('testuser1', PortalUser.objects.get(id=self.user.id).username)

    def test_user_profile_update_data_without_password(self):
        self.client.login(username=self.user.username, password=self.user_credentials['password'])

        data = {
            'username': 'testuser1',
            'password': '',
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
            'phone': '06086304638',
            'email': 'testuser@newmail.com',
        }

        response = self.client.post(
            '/user/profile/',
            data=data,
        )
        self.assertEqual(self.REDIRECT_RESPONSE_CODE, response.status_code)
        
        self.assertEqual('testuser1', PortalUser.objects.get(id=self.user.id).username)
