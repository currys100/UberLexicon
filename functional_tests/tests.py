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

    def test_home_page_loads(self):
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('UberLexicon', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('UberLexicon', header_text)

    def test_can_add_item_for_one_user(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('kaizen')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_appropriate_duration('1: kaizen')

        # Alir wants to enter another word.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('genki')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_appropriate_duration('1: kaizen')
        self.wait_for_appropriate_duration('2: genki')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_appropriate_duration('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/words/.+/')

        # Now a new user, Francis, comes along to the site.
        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_appropriate_duration('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/words/.+/')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

