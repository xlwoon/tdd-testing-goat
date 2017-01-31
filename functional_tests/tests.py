from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(firefox_binary = FirefoxBinary(firefox_path = '/home/woon/Documents/learn/TDD/testing-goat/firefox/firefox'))
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
    # Uma has heard about this cool new website, an automated to-do list
    # she fires up a browser to check out it's home page
        self.browser.get(self.live_server_url)

    # she notices it indicates clearly it's a to-do app
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

    # she is immediately invited to add an item to the to-do list
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual( inputbox.get_attribute('placeholder'), 'Enter a to-do item' )

    # she types "buy frozen pizza" into a text box
        inputbox.send_keys('Buy frozen pizza')
    # Uma loves frozen pizza

    # when she submits the contents, the page updates and lists
    # "1: buy frozen pizza" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy frozen pizza')

    # the updated page also contains a text box for further items to be added
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual( inputbox.get_attribute('placeholder'), 'Enter a to-do item' )

    # Uma adds "eat frozen pizza" into the text box
    # she doesn't want to forget
        inputbox.send_keys('Eat frozen pizza')
        inputbox.send_keys(Keys.ENTER)

    # when the page updates again, it contains both items

        self.check_for_row_in_list_table('1: Buy frozen pizza')
        self.check_for_row_in_list_table('2: Eat frozen pizza')

    # Uma wonders if the site will remember her list
    def test_multiple_users_can_start_lists_at_different_urls(self):

        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy frozen pizza')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy frozen pizza')

    # it does: and generates a unique URL for it
        uma_list_url = self.browser.current_url
        self.assertRegex(uma_list_url, '/lists/.+')


    # a new user, Ulrich comes along.
    ## we use a new browser session to make sure none of Uma's data is coming through from cookies
        self.browser.quit()
        self.browser = webdriver.Firefox(firefox_binary = FirefoxBinary(firefox_path = '/home/woon/Documents/learn/TDD/testing-goat/firefox/firefox'))
        self.browser.implicitly_wait(5)

    # Ulrich visits homepage and sees no trace of Uma's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy frozen pizza', page_text)
        self.assertNotIn('Eat frozen pizza', page_text)

    # Ulrich starts his own list by entering items
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy eggs')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy eggs')

    # Ulrich's list gets a unique URL
        ulrich_list_url = self.browser.current_url
        self.assertRegex(ulrich_list_url, '/lists/.+')
        self.assertNotEqual(ulrich_list_url, uma_list_url)

    # There is still no trace of Uma's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy frozen pizza', page_text)
        self.assertNotIn('Eat frozen pizza', page_text)

    # also displays some explanatory text about that

    # she double checks the URL works, and that her list is displayed

    # satisfied, she goes to sleep, dreaming of pizza




    def test_layout_and_styling(self):

    # new user goes to homepage
        self.browser.get(self.live_server_url)
        window_size = self.browser.get_window_size()
        window_width = window_size["width"]

    # and notices the input box is nicely centered!
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, window_width/2, delta = 5)

    # new user starts a new list and sees input is nicely centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, window_width/2, delta = 5)
