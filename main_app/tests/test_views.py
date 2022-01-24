from django.core.paginator import Paginator
from django.test import TestCase
from django.test.client import Client

from company_app.models import Company
from news_app.models import News


class MainAppTestCase(TestCase):
    client = Client()
    companies = Company.objects.all()
    news_list = News.objects.get_queryset().order_by('id')
    paginator = Paginator(news_list, 2)

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
