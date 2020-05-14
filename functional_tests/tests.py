"""
Functional tests for the UberLexicon

date: 05-2020
author: Sarah K. Curry

Notes:
    Initially I had installed geckdriver in my local project directory (~/UberLexicon/.). Even though this
directory is included in $PATH, I repeatedly got the error that << selenium.common.exceptions.WebDriverException:
Message: 'geckodriver' executable needs to be in PATH. >> I tried exporting PATH to add the current directory,
and reinstalled geckodriver, but to no avail. I finally resolved the problem by moving geckodriver to /usr/local/bin,
as directed here: https://stackoverflow.com/questions/40388503/how-to-put-geckodriver-into-path/40392714

To Do:
- clear test database as part of teardown.

"""

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 4  #seconds


# noinspection SpellCheckingInspection
class NewVisitorTest(LiveServerTestCase):
    """
    Functional tests to determine if database and website are launched according to plan.
    """

    def setUp(self):
        self.browser = webdriver.Firefox()

    def wait_for_appropriate_duration(self, row_text):
        """
        Input:
            row_text (str): new word entered by user

        :rtype: bool
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_word_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (WebDriverException, AssertionError) as e:
                if time.time() - start_time > MAX_WAIT:
                    print("exceeded max time")
                    raise e
                time.sleep(0.5)

    def tearDown(self):
        self.browser.quit()

    # def test_open_browser(self):
    #     self.browser.get('http://localhost:8000')
    #     self.assertIn('UberLexicon', self.browser.title)

    def test_add_new_word_to_db(self):
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('UberLexicon', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('UberLexicon', header_text)

        # Alir wants to add a new word to the db.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a word')

        # Alir adds the word 'kaizen'
        inputbox.send_keys('kaizen')

        # When she hits enter, the page updates, and now the page lists
        # "kaizen" as an item in a lexicon table
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_appropriate_duration('1: kaizen')

        # Alir wants to enter another word.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('genki')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_appropriate_duration('1: kaizen')
        self.wait_for_appropriate_duration('2: genki')

        self.fail("Finish the test!")

    # def test_add_definition_for_new_word(self):
    #     inputbox_definition = self.browser.find_element_by_id('id_item_definition')
    #     definition_text = 'incremental and continual improvement'
    #     inputbox_definition.send_keys(definition_text)
    #     inputbox_definition.send_keys(Keys.ENTER)
    #
    #     self.wait_for_appropriate_duration('1: kaizen', definition_text)
    #
    #     self.fail("Finish the test!")


    # Alir wants to search the db for a specific word by name.
    # Alir searches the db for all words in Japanese.
    # Alir views all words in the db.
