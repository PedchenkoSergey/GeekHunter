from django.test import TestCase

from auth_app.models import PortalUser
from company_app.models import Card, Company, Vacancy, Offer, HrManager


class CompanyAppModelsTestCase(TestCase):
    def setUp(self) -> None:
        self.test_user = PortalUser.objects.create(phone='123456', email='user@geekhunter.com')
        self.company_1 = Company.objects.create(name='company_1', short_description='descr', specialization='IT')
        self.company_1_card = Card.objects.create(
            title='test title',
            company_id=self.company_1.id,
            about='test about',
            awards='test awards',
            priorities='test priorities',
            status='ACTIVE',
            moderation_status='APPROVED',
            company=self.company_1
        )
        self.vacancy_1 = Vacancy.objects.create(
            company=self.company_1,
            company_id=self.company_1.id,
            title='test vacancy',
            salary='8000',
            description='test descr',
            moderation_status='APPROVED',
            status='ACTIVE',
        )
        self.offer_1 = Offer.objects.create(
            title='test offer 1',
            status='SENT',
            vacancy=self.vacancy_1,
            vacancy_id=self.vacancy_1.id
        )
        self.hr_manager_1 = HrManager.objects.create(
            first_name='hr',
            last_name='manager',
            email='hr@manager.com',
            company=self.company_1,
            company_id=self.company_1.id,
            user_id=self.test_user.id
        )

    def test_company_str(self):
        self.assertEqual('company_1', str(Company.objects.get(id=1)))

    def test_card_str(self):
        self.assertEqual('test title', str(Card.objects.get(id=1)))

    def test_vacancy_str(self):
        self.assertEqual('test vacancy', str(Vacancy.objects.get(id=1)))

    def test_offer_str(self):
        self.assertEqual('test offer 1 SENT', str(Offer.objects.get(id=1)))

    def test_hr_manager_str(self):
        self.assertEqual('hr manager', str(HrManager.objects.get(id=1)))
