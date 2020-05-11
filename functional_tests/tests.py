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


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


# noinspection SpellCheckingInspection
class TestLaunchingDatabase(unittest.TestCase):
    """
    Functional tests to determine if database and website are launched according to plan.
    """

    def setUp(self):
        self.browser = webdriver.Firefox()

    def check_for_row_in_list_table(self, row_text):
        """
        Input:
            row_text (str): new word entered by user

        :rtype: object
        """
        table = self.browser.find_element_by_id('id_word_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def tearDown(self):
        self.browser.quit()

    # def test_open_browser(self):
    #     self.browser.get('http://localhost:8000')
    #     self.assertIn('UberLexicon', self.browser.title)

    def test_add_new_word_to_db(self):
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)
        self.check_for_row_in_list_table('1: kaizen')

        # Alir wants to enter another word.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('genki')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: kaizen')
        self.check_for_row_in_list_table('2: genki')


    # Alir wants to search the db for a specific word by name.
    # Alir searches the db for all words in Japanese.
    # Alir views all words in the db.

if __name__ == '__main__':
    unittest.main(warnings='ignore')



    # def test_django_selenium_geckodriver_installed(self):
    #     geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
    #     # and if it doesn't exist, download it automatically,
    #     # then add geckodriver to path
    #
    #     driver = webdriver.Firefox()
    #     driver.get("http://www.python.org")
    #     assert "Python" in driver.title