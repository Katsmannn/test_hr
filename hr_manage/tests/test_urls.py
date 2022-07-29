from django.test import Client, TestCase

from http import HTTPStatus


class MyURLTests(TestCase):
    databases = {'test_sqlite'}
    def setUp(self):
        self.client = Client()

    def test_urls(self):
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_page_not_found_status(self):
        response = self.client.get('/wrong_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
