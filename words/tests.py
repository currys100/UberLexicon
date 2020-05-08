"""
Unit tests for lists.
"""

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from words.views import home_page
from django.template.loader import render_to_string


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new word item'})
        self.assertIn('A new word item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

# class SmokeTest(TestCase):
#
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)