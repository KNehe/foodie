from django.test import TestCase

from fapp.forms import PostForm

class PostFormTests(TestCase):
    def test_post_form(self):
         """
         Form should be valid when given correct data
         """
         form_data = {'foodie': 'Boil water for 10 mins'}
         form = PostForm(data=form_data)
         self.assertTrue(form.is_valid())
    
    def test_post_form_empty_field(self):
        """
        Form should be invalid when data is not provided
        """
        form = PostForm()
        self.assertFalse(form.is_valid())
    
    def test_extra_characters(self):
        """
        Should fail when charactars are more than 200
        """
        form_data = {'foodie': 'A very long string A very long string A very long string A very long string A very long stringA very long stringA very long stringA very long stringA very long stringA very long stringA very long string'}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
