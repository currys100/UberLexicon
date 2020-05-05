"""
Functional tests for the UberLexicon

date: 05-2020
author: Sarah K. Curry
"""

import unittest
from selenium import webdriver

from selenium import webdriver
import geckodriver_autoinstaller


class TestLaunchingDatabase(unittest.TestCase):

    def test_django_selenium_geckodriver_installed(self):
        geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
        # and if it doesn't exist, download it automatically,
        # then add geckodriver to path

        driver = webdriver.Firefox()
        driver.get("http://www.python.org")
        assert "Python" in driver.title

    def test_open_browser(self):
        browser = webdriver.Firefox()
        browser.get('https://www.djangoproject.com/')
        assert 'Django' in browser.title


if __name__ == '__main__':
    unittest.main()
