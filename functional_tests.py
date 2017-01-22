from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(firefox_binary = FirefoxBinary(firefox_path = '/home/woon/Documents/learn/TDD/testing-goat/firefox/firefox'))
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
    # Uma has heard about this cool new website, an automated to-do list
    # she fires up a browser to check out it's home page
        self.browser.get('http://localhost:8000')

    # she notices it indicates clearly it's a to-do app
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

    # she is immediately invited to add an item to the to-do list

    # she types "buy frozen pizza" into a text box
    # Uma loves frozen pizza

    # when she submits the contents, the page updates and lists
    # "1: buy frozen pizza" as an item in a to-do list

    # the updated page also contains a text box for further items to be added

    # Uma adds "eat frozen pizza" into the text box
    # she doesn't want to forget

    # when the page updates again, it contains both items

    # Uma wonders if the site will remember her list
    # it does: and generates a unique URL for it
    # also displays some explanatory text about that

    # she double checks the URL works, and that her list is displayed

    # satisfied, she goes to sleep, dreaming of pizza

if __name__ == '__main__':
    unittest.main(warnings='ignore')
