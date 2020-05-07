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

"""

import unittest
from selenium import webdriver

class TestLaunchingDatabase(unittest.TestCase):

    # def test_django_selenium_geckodriver_installed(self):
    #     geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
    #     # and if it doesn't exist, download it automatically,
    #     # then add geckodriver to path
    #
    #     driver = webdriver.Firefox()
    #     driver.get("http://www.python.org")
    #     assert "Python" in driver.title

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_open_browser(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Django', self.browser.title)
        # self.fail("Finish the test!")


    # Alir wants to add a new word to the db.
    # Alir wants to search the db for a specific word by name.
    # Alir searches the db for all words in Japanese.
    # Alir views all words in the db.


if __name__ == '__main__':
    unittest.main(warnings='ignore')

