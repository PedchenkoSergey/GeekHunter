from django.contrib.auth.models import Permission
from django.test import TestCase
from django.test.client import Client

from auth_app.models import PortalUser
from company_app.models import Company, Card, Vacancy, HrManager
from employee_app.models import FavoriteVacancies, Employee


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

        self.hr_credentials = {
            'username': 'company',
            'email': 'company@geekhunter.com',
            'phone': '987789',
            'password': 'password',
        }

        self.approved_and_active_vacancy_credentials = {
            'title': 'awesome work',
            'company': self.company_1,
            'description': 'hello',
            'salary': 1000,
            'status': 'ACTIVE',
            'moderation_status': 'APPROVED',
        }

        self.new_vacancy_credentials = {
            'title': 'new job',
            'company': self.company_1,
            'description': 'test description',
            'salary': 200,
            'location': 'Anything',
            'status': 'ACTIVE',
        }

        self.user = PortalUser.objects.create_user(**self.user_credentials)

        self.hr = PortalUser.objects.create_user(**self.hr_credentials)

        self.employee = Employee.objects.create(user=self.user)

        self.hr_manager = HrManager.objects.create(user=self.hr)

        self.vacancy = Vacancy.objects.create(**self.approved_and_active_vacancy_credentials)

        self.favorite_vacancy = FavoriteVacancies.objects.create(
            employee=self.employee, vacancy=self.vacancy
        )

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

    def test_exact_company_vacancies_for_user_has_perm(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_vacancy'))
        self.client.login(username='employee', password="password")
        response = self.client.get(f'/company/vacancies/{self.company_1.id}/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_vacancies_for_user_has_no_perm(self):
        self.client.login(username='employee', password="password")
        response = self.client.get('/company/vacancies')
        self.assertEqual(self.PERMISSON_DENIED_CODE, response.status_code)

    def test_view_favorite_vacancies_200(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_vacancy'))
        self.client.login(username='employee', password="password")

        response = self.client.get('/company/vacancies')

        self.assertEqual(response.context_data['favorite_vacancies'][0].id, self.favorite_vacancy.id)
        self.assertEqual(
            response.context_data['favorite_vacancies'][0].vacancy.company,
            self.favorite_vacancy.vacancy.company
        )
        self.assertEqual(response.context_data['favorite_vacancies'][0].employee, self.favorite_vacancy.employee)

    def test_view_company_profile_ok(self):
        self.client.login(username=self.hr.username, password=self.hr_credentials['password'])

        response = self.client.get('/company/profile/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_view_profile_vacancies_ok(self):
        self.client.login(username=self.hr.username, password=self.hr_credentials['password'])

        response = self.client.get('/company/profile/vacancies/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_view_profile_vacancies_create_ok(self):
        self.client.login(username=self.hr.username, password=self.hr_credentials['password'])

        response = self.client.get('/company/profile/vacancies/create/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_view_profile_card_ok(self):
        self.client.login(username=self.hr.username, password=self.hr_credentials['password'])

        response = self.client.get(f'/company/profile/card/edit/{self.company_1.id}/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_view_profile_vacancies_create_post(self):
        self.client.login(username=self.hr.username, password=self.hr_credentials['password'])

        response = self.client.post(
            '/company/profile/vacancies/create/',
            data=self.new_vacancy_credentials
        )
        self.assertEqual(self.REDIRECT_RESPONSE_CODE, response.status_code)
        new_vacancy = Vacancy.objects.get(title=self.new_vacancy_credentials['title'])
        self.assertEqual(self.new_vacancy_credentials['title'], new_vacancy.title)

    def test_view_favorite_vacancies_create(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_vacancy'))
        self.client.login(username='employee', password="password")

        response = self.client.post('/company/vacancies', data={'vacancy': self.vacancy.id})

        self.assertEqual(self.REDIRECT_RESPONSE_CODE, response.status_code)
