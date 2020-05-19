"""
Unit tests for words.
"""

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from words.views import home_page, view_words
from django.template.loader import render_to_string
from words.models import Item, Word


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


class WordAndItemModelTest(TestCase):
    """
    Test creation of Word and Item classes.
    TestCase does not interact with browser.
    """

    def test_saving_and_retrieving_items(self):
        word_ = Word()
        word_.save()
        first_item = Item()
        first_item.text = 'kaizen'
        first_item.word = word_
        first_item.save()

        second_item = Item()
        second_item.text = 'genki'
        second_item.word = word_
        second_item.save()

        saved_words = Word.objects.first()
        self.assertEqual(saved_words, word_)

        saved_items = Item.objects.all()
        self.assertEqual(2, saved_items.count())

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'kaizen')
        self.assertEqual(second_saved_item.text, 'genki')
        self.assertEqual(first_saved_item.word, word_)
        self.assertEqual(second_saved_item.word, word_)


class WordViewTest(TestCase):

    def test_uses_words_template(self):
        word_ = Word.objects.create()
        response = self.client.get(f'/words/{word_.id}/')
        # print(response.context['word_.id'])
        self.assertTemplateUsed(response, 'words.html')

    def test_retrieving_items_from_db(self):
        test_word = Word.objects.create()
        Item.objects.create(text='itemey 1', word=test_word)
        Item.objects.create(text='itemey 2', word=test_word)

        saved_words = Word.objects.all()
        self.assertEqual(saved_words.count(), 1)

    def test_passes_words_to_correct_list(self):
        correct_list = Word.objects.create()
        wrong_list = Word.objects.create()

        response = self.client.get(f'/words/{correct_list.id}/')

        self.assertEqual(response.context['word'], correct_list)

    def test_displays_only_items_for_that_word(self):
        correct_word = Word.objects.create()
        Item.objects.create(text='itemey 1', word=correct_word)
        Item.objects.create(text='itemey 2', word=correct_word)
        other_word = Word.objects.create()
        Item.objects.create(text='other word item 1', word=other_word)
        Item.objects.create(text='other word item 2', word=other_word)

        response = self.client.get(f'/words/{correct_word.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other word item 1')
        self.assertNotContains(response, 'other word item 2')


class NewItemTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/words/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = Word.objects.create()
        correct_list = Word.objects.create()

        self.client.post(
            f'/words/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.word, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = Word.objects.create()
        other_list = Word.objects.create()

        response = self.client.post(
            f'/words/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/words/{correct_list.id}/')