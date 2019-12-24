import unittest
from selenium import webdriver
from django.test import TestCase

import time

URL = "http://raplev.com:8080"


class SellVisitorTest (TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_user_signup_and_login(self):
        # Omar needs to use Raplev for his job. He goes
        # to check out its homepage
        self.browser.get(URL)

        # He notices the page title and header mention Raplev
        self.assertIn('Homepage', self.browser.title)

        # He notices a registration button
        signup_button = self.browser.find_element_by_xpath('/html/body/header/div/div[1]/nav/ul/li[3]/button')
        signup_button.click()

        # The Registration pane is opened
        # where he enters a username and a password
        username_field = self.browser.find_element_by_id('email')
        name_field = self.browser.find_element_by_id('full_name')
        password1_field = self.browser.find_element_by_id('password1')
        password2_field = self.browser.find_element_by_id('password2')

        # He wants to sell
        sign_up_button = self.browser.find_element_by_id('buy_button')

        # He fills in the details for a new user and clicks on the "Sign Up" button
        username_field.send_keys('test1@example.com')
        name_field.send_keys('test test')
        password1_field.send_keys('test1test1')
        password2_field.send_keys('test1test1')
        sign_up_button.click()
        time.sleep(3)


class BuyVisitorTest (TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_user_signup_and_login(self):
        # Omar needs to use Raplev for his job. He goes
        # to check out its homepage
        self.browser.get(URL)

        # He notices the page title and header mention Raplev
        self.assertIn('Homepage', self.browser.title)

        # He notices a registration button
        signup_button = self.browser.find_element_by_xpath('/html/body/header/div/div[1]/nav/ul/li[3]/button')
        signup_button.click()

        # The Registration pane is opened
        # where he enters a username and a password
        username_field = self.browser.find_element_by_id('email')
        name_field = self.browser.find_element_by_id('full_name')
        password1_field = self.browser.find_element_by_id('password1')
        password2_field = self.browser.find_element_by_id('password2')

        # He wants to sell
        sign_up_button = self.browser.find_element_by_id('sell_button')

        # He fills in the details for a new user and clicks on the "Sign Up" button
        username_field.send_keys('test1@example.com')
        name_field.send_keys('test test')
        password1_field.send_keys('test1test1')
        password2_field.send_keys('test1test1')
        sign_up_button.click()
        time.sleep(3)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
if __name__ == '__main__':
    unittest.main(warnings='ignore')
