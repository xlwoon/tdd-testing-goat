from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.models import Item, List
from lists.views import home_page

# Create your tests here.

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
       # list_ = List()
       # list_.save()

        list_ = List.objects.create()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Second item, directly after first'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual('The first (ever) list item', first_saved_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual('Second item, directly after first', second_saved_item.text)
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' %(list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_specified_list_items(self):
        target_list = List.objects.create()
        Item.objects.create(text='doodad 1', list=target_list)
        Item.objects.create(text='doodad 2', list=target_list)
        another_list = List.objects.create()
        Item.objects.create(text='widget 1', list=another_list)
        Item.objects.create(text='widget 2', list=another_list)

        response = self.client.get('/lists/%d/' %(target_list.id))

        self.assertContains(response, 'doodad 1')
        self.assertContains(response, 'doodad 2')
        self.assertNotContains(response, 'widget 1')
        self.assertNotContains(response, 'widget 2')

class NewListTestCase(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'a new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'a new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'a new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' %(new_list.id))

class NewItemTest(TestCase):

    def test_can_save_a_POST_to_existing_list(self):
        target_list = List.objects.create()
        some_other_list = List.objects.create()

        self.client.post('/lists/%d/add_item' %(target_list.id), data={'item_text': 'an additional item to an existing list'} )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'an additional item to an existing list')
        self.assertEqual(new_item.list, target_list)

    def test_redirects_to_list_view(self):
        target_list = List.objects.create()
        some_other_list = List.objects.create()

        response = self.client.post('/lists/%d/add_item' %(target_list.id), data={'item_text': 'an additional item to an existing list'} )

        self.assertRedirects(response, '/lists/%d/' %(target_list.id))

    def test_passes_correct_list_to_template(self):
        target_list = List.objects.create()
        some_other_list = List.objects.create()

        response = self.client.get('/lists/%d/' %(target_list.id))
        self.assertEqual(response.context['list'], target_list)
