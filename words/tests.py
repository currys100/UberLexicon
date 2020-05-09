"""
Unit tests for lists.
"""

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from words.views import home_page
from django.template.loader import render_to_string
from words.models import Item


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new word item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new word item')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_db_only_saves_items_when_necessary(self):
        self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_displaying_multiple_items(self):
        Item.objects.create(text='dolphin1')
        Item.objects.create(text='echo2')

        response = self.client.get('/')

        self.assertIn('dolphin1', response.content.decode())
        self.assertIn('echo2', response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'kaizen'
        first_item.save()

        second_item = Item()
        second_item.text = 'genki'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(2, saved_items.count())

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'kaizen')
        self.assertEqual(second_saved_item.text, 'genki')



# class SmokeTest(TestCase):
#
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)