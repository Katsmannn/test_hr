from http import HTTPStatus

from django.test import Client, TestCase


class MyURLTests(TestCase):
    databases = {'test_sqlite'}
    def setUp(self):
        self.client = Client()

    def test_correct_urls(self):
        urls_statuses = {
            HTTPStatus.OK: [
                '/employees/',
                '/employees/new/',
                '/positions/',
                '/positions/new/',
            ],
            HTTPStatus.FOUND: [
                '/employees/1/delete',
                '/positions/1/delete',
            ]
        }

        for status, urls in urls_statuses.items():
            for url in urls:
                with self.subTest(url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_page_not_found_status(self):
        response = self.client.get('/wrong_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
