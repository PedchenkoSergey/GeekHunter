import json

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.test.client import Client

from auth_app.models import PortalUser
from company_app.models import Company, Card, Vacancy, HrManager, FavoriteResume
from employee_app.models import FavoriteVacancies, Employee, Resume, Experience, Education, Courses


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

        self.experience_credentials = {
            'company': 'test company',
            'period': 'test period',
            'position': 'test position',
            'duties': 'test duties',
            'resume': self.resume,
        }

        self.experience = Experience.objects.create(**self.experience_credentials)

        self.education_credentials = {
            'educational_institution': 'test institution',
            'specialization': 'test specialization',
            'year_of_ending': '2022',
            'resume': self.resume,
        }

        self.education = Education.objects.create(**self.education_credentials)

        self.courses_credentials = {
            'company': 'test company',
            'specialization': 'test specialization',
            'year_of_ending': '2022',
            'resume': self.resume,
        }

        self.courses = Courses.objects.create(**self.courses_credentials)

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

    def test_view_employee_profile_ok(self):
        self.client.login(username=self.employee.user.username, password=self.user_credentials['password'])

        response = self.client.get('/employee/profile/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_view_employee_profile_resumes_ok(self):
        self.client.login(username=self.employee.user.username, password=self.user_credentials['password'])

        response = self.client.get('/employee/profile/resumes/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_view_employee_profile_resume_create_ok(self):
        self.client.login(username=self.employee.user.username, password=self.user_credentials['password'])

        response = self.client.get('/employee/profile/resumes/create/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_view_employee_profile_resume_read_ok(self):
        self.client.login(username=self.employee.user.username, password=self.user_credentials['password'])

        response = self.client.get(f'/employee/profile/resumes/read/{self.resume.id}/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_view_employee_profile_resume_edit_ok(self):
        self.client.login(username=self.employee.user.username, password=self.user_credentials['password'])

        response = self.client.get(f'/employee/profile/resumes/edit/{self.resume.id}/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_view_employee_profile_resume_delete_ok(self):
        self.client.login(username=self.employee.user.username, password=self.user_credentials['password'])

        response = self.client.get(f'/employee/profile/resumes/delete/{self.resume.id}/')
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_employee_profile_delete_entity_from_resume(self):
        self.client.login(username=self.employee.user.username, password=self.user_credentials['password'])

        data = {
            'model': 'experience',
            'pk': self.experience.pk,
        }

        self.assertEqual(1, len(Experience.objects.all()))

        response = self.client.post(
            '/employee/profile/resume/entity_delete/',
            json.dumps(data),
            content_type='application/json',
            xhr=True,
        )
        self.assertEqual(0, len(Experience.objects.all()))
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

    def test_employee_profile_resume_create(self):
        self.client.login(username=self.employee.user.username, password=self.user_credentials['password'])

        data = {
            'title': 'new resume',
            'status': 'ACTIVE',
            'fields': {
                'experience': [{
                    'company': 'new company',
                    'period': 'somee period',
                    'position': 'dev',
                    'duties': 'coding',
                }],
                'education': [{
                    'educational_institution': 'new institution',
                    'specialization': 'new specialization',
                    'year_of_ending': '2023',
                }],
                'courses': [{
                    'company': 'new courses company',
                    'specialization': 'new specialization',
                    'year_of_ending': '2024',
                }],
            },
        }

        self.assertEqual(1, len(Resume.objects.all()))
        self.assertEqual(1, len(Experience.objects.all()))
        self.assertEqual(1, len(Education.objects.all()))
        self.assertEqual(1, len(Courses.objects.all()))

        response = self.client.post(
            '/employee/profile/resumes/create/',
            json.dumps(data),
            content_type='application/json',
            xhr=True,
        )
        self.assertEqual(self.REDIRECT_RESPONSE_CODE, response.status_code)

        self.assertEqual(2, len(Resume.objects.all()))
        self.assertEqual(2, len(Experience.objects.all()))
        self.assertEqual(2, len(Education.objects.all()))
        self.assertEqual(2, len(Courses.objects.all()))

    def resume_edit_start(self):
        self.client.login(username=self.employee.user.username, password=self.user_credentials['password'])

        resume = Resume.objects.get(id=self.resume.id)
        experience = Experience.objects.get(resume=resume)
        education = Education.objects.get(resume=resume)
        courses = Courses.objects.get(resume=resume)

        self.assertEqual('awesome worker', str(resume))
        self.assertEqual('test position', str(experience))
        self.assertEqual('test institution', str(education))
        self.assertEqual('test company', str(courses))

    def test_employee_profile_resume_edit(self):
        self.resume_edit_start()

        data = {
            'pk': self.resume.id,
            'title': 'super worker',
            'status': 'ACTIVE',
            'fields': {
                'experience': [{
                    'company': 'company',
                    'period': 'somee period',
                    'position': 'driver',
                    'duties': 'drive',
                    'pk': self.experience.pk,
                }],
                'education': [{
                    'educational_institution': 'СПбГУ',
                    'specialization': 'сантехник',
                    'year_of_ending': '2023',
                    'pk': self.education.pk,
                }],
                'courses': [{
                    'company': 'GeekBrains',
                    'specialization': 'python dev',
                    'year_of_ending': '2024',
                    'pk': self.courses.pk,
                }],
            },
        }
        response = self.client.post(
            f'/employee/profile/resumes/edit/{self.resume.id}/',
            json.dumps(data),
            content_type='application/json',
            xhr=True,
        )
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

        updated_resume = Resume.objects.get(id=self.resume.id)
        updated_experience = Experience.objects.get(resume=updated_resume)
        updated_education = Education.objects.get(resume=updated_resume)
        updated_courses = Courses.objects.get(resume=updated_resume)

        self.assertEqual('super worker', str(updated_resume))
        self.assertEqual('driver', str(updated_experience))
        self.assertEqual('СПбГУ', str(updated_education))
        self.assertEqual('GeekBrains', str(updated_courses))

    def test_employee_profile_resume_edit_add_entity(self):
        self.resume_edit_start()

        data = {
            'pk': self.resume.id,
            'title': 'awesome worker',
            'status': 'ACTIVE',
            'fields': {
                'experience': [{
                    'company': 'tesla',
                    'period': '2012-2022',
                    'position': 'dev',
                    'duties': 'coding',
                    'pk': '0',
                }],
            },
        }

        self.assertEqual(1, len(Experience.objects.all()))

        response = self.client.post(
            f'/employee/profile/resumes/edit/{self.resume.id}/',
            json.dumps(data),
            content_type='application/json',
            xhr=True,
        )
        self.assertEqual(self.SUCCESS_RESPONSE_CODE, response.status_code)

        self.assertEqual(2, len(Experience.objects.all()))

        new_experience = Experience.objects.get(company='tesla')

        self.assertEqual('dev', new_experience.position)
