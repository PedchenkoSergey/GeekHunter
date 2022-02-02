from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import Permission

from auth_app.models import PortalUser
from company_app.models import Company, Card, Vacancy


class CompanyAppTestCase(TestCase):
    SUCCESS_RESPONSE_CODE = 200
    REDIRECT_RESPONSE_CODE = 302
    PERMISSON_DENIED_CODE = 403
    PAGE_NOT_FOUND_CODE = 404

    def setUp(self) -> None:
        self.client = Client()
        self.company_1 = Company.objects.create(name='company_1', short_description='descr', specialization='IT')
        self.company_2 = Company.objects.create(name='company_2', short_description='descr', specialization='IT')
        self.company_3 = Company.objects.create(name='company_3', short_description='descr', specialization='IT')
        self.company_1_card_approved_and_active = Card.objects.create(
            company=self.company_1,
            company_id=self.company_1.id,
            title='test title',
            about='test about',
            awards='test awards',
            priorities='test priorities',
            status='ACTIVE',
            moderation_status='APPROVED',
        )
        self.company_2_card_not_approved_and_active = Card.objects.create(
            company=self.company_2,
            company_id=self.company_2.id,
            title='test title 2',
            about='test about 2',
            awards='some awards 2',
            priorities='test priorities 2',
            status='ACTIVE',
            moderation_status='UNDER_REVIEW',
        )
        self.company_3_card_approved_and_not_active = Card.objects.create(
            company=self.company_3,
            company_id=self.company_3.id,
            title='test title 3',
            about='test about 3',
            awards='some awards 3',
            priorities='test priorities 3',
            status='DRAFT',
            moderation_status='APPROVED',
        )

        self.user_credentials = {
            'username': 'employee',
            'email': 'employee@geekhunter.com',
            'phone': '2345',
            'password': 'password',
        }

        self.user = PortalUser.objects.create_user(**self.user_credentials)

    def test_company_card_page_approved_and_active_ok(self):
        response = self.client.get('/company/1/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_company_card_page_not_approved_and_active_ok(self):
        response = self.client.get('/company/2/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_company_card_page_approved_and_not_active_ok(self):
        response = self.client.get('/company/3/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_company_card_404(self):
        response = self.client.get(f'/company/{Company.objects.all().count() + 1}/')
        self.assertEqual(self.PAGE_NOT_FOUND_CODE, response.status_code)

    def test_vacancies_redirect_anonymous(self):
        response = self.client.get('/company/vacancies')
        self.assertEqual(self.REDIRECT_RESPONSE_CODE, response.status_code)

    def test_vacancies_for_user_has_perm(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_vacancy'))
        self.client.login(username='employee', password="password")
        response = self.client.get('/company/vacancies')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_vacancies_for_user_has_no_perm(self):
        self.client.login(username='employee', password="password")
        response = self.client.get('/company/vacancies')
        self.assertEqual(self.PERMISSON_DENIED_CODE, response.status_code)

