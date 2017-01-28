from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.models import Item
from lists.views import home_page

# Create your tests here.

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'a new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'a new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'a new list item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='thingy 1')
        Item.objects.create(text='thingy 2')

        response = self.client.get('/')

        self.assertIn('thingy 1', response.content.decode())
        self.assertIn('thingy 2', response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Second item, directly after first'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual('The first (ever) list item', first_saved_item.text)
        self.assertEqual('Second item, directly after first', second_saved_item.text)
