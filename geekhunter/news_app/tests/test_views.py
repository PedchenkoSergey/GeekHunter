from django.core.paginator import Paginator
from django.test import TestCase
from django.test.client import Client

from news_app.models import News


class MainAppTestCase(TestCase):

    def setUp(self) -> None:
        client = Client()

        self.news_list = News.objects.get_queryset().order_by('id')
        self.paginator = Paginator(self.news_list, 2)


    def test_news_page_not_a_int(self):
        response = self.client.get('/?page=str')
        self.assertEqual(200, response.status_code)

    def test_news_empty_page(self):
        response = self.client.get(f'/?page={self.paginator.num_pages + 1}')
        self.assertEqual(200, response.status_code)


# TODO: может сделать много новостей