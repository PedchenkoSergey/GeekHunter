from django.contrib.auth.models import Permission
from django.test import TestCase
from django.test.client import Client

from auth_app.models import PortalUser
from company_app.models import Company, Card, Vacancy, HrManager, FavoriteResume
from employee_app.models import FavoriteVacancies, Employee, Resume


class EmployeeAppTestCase(TestCase):
    SUCCESS_RESPONSE_CODE = 200
    REDIRECT_RESPONSE_CODE = 302
    PERMISSON_DENIED_CODE = 403
    PAGE_NOT_FOUND_CODE = 404

    def setUp(self) -> None:
        self.client = Client()
        self.company_1 = Company.objects.create(name='company_1', short_description='descr', specialization='IT')

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

        self.user_credentials = {
            'username': 'mycompany',
            'email': 'mycompany@geekhunter.com',
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

        self.user = PortalUser.objects.create_user(**self.user_credentials)

        self.employee = Employee.objects.create(user=self.user)

        self.active_resume_credentials = {
            'title': 'awesome worker',
            'employee': self.employee,
            'status': 'ACTIVE',
        }

        self.new_vacancy_credentials = {
            'title': 'new job',
            'company': self.company_1,
            'description': 'test description',
            'salary': 200,
            'location': 'Anything',
            'status': 'ACTIVE',
        }

        self.hr_manager = HrManager.objects.create(user=self.user)

        self.vacancy = Vacancy.objects.create(**self.approved_and_active_vacancy_credentials)

        self.resume = Resume.objects.create(**self.active_resume_credentials)

        self.favorite_vacancy = FavoriteVacancies.objects.create(
            employee=self.employee, vacancy=self.vacancy
        )

        self.favorite_resume = FavoriteResume.objects.create(
            hr_manager=self.hr_manager, resume=self.resume
        )

    def test_vacancies_redirect_anonymous(self):
        response = self.client.get('/employee/resumes')

        self.assertEqual(self.REDIRECT_RESPONSE_CODE, response.status_code)

    def test_resumes_page_for_user_has_perm_list(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_resume'))
        self.client.login(username='mycompany', password="password")

        response = self.client.get('/employee/resumes')

        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)
        self.assertEqual(response.context_data['resumes'][0].id, self.resume.id)

    def test_resumes_page_for_user_has_perm_detail(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_resume'))
        self.client.login(username='mycompany', password="password")

        response = self.client.get(f'/employee/resumes/{self.employee.pk}/')

        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_resumes_page_for_user_has_no_perm(self):
        self.client.login(username='mycompany', password="password")

        response = self.client.get('/employee/resumes')

        self.assertEqual(self.PERMISSON_DENIED_CODE, response.status_code)

    def test_view_favorite_resumes_200(self):
        self.user.user_permissions.add(Permission.objects.get(codename='view_resume'))
        self.client.login(username='mycompany', password="password")

        response = self.client.get('/employee/resumes')

        self.assertEqual(response.context_data['favorite_resumes'][0].id, self.favorite_resume.id)
        self.assertEqual(
            response.context_data['favorite_resumes'][0].hr_manager,
            self.favorite_resume.hr_manager
        )
