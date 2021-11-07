from django.test import TestCase

from fapp.forms import PostForm, CustomUserCreationForm

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

class CustomUserRegistrationFormTests(TestCase):
    def test_all_fields_are_valid(self):
        form_data = {"username": "nehe",
                     "password1": "ABCDe124",
                     "password2": "ABCDe124",
                     "email": "nehe@gmail.com"}
        form =  CustomUserCreationForm(form_data)

        self.assertTrue(form.is_valid())
    
    def test_all_passwords_not_equal(self):
        form_data = {"username": "nehe",
                     "password1": "ABCDe124",
                     "password2": "ABCDe12423",
                     "email": "nehe@gmail.com"}
        form =  CustomUserCreationForm(form_data)
        
        self.assertEqual(form.error_messages, {'password_mismatch': 'The two password fields didn’t match.'})
        self.assertFalse(form.is_valid())
    
    def test_all_fields_are_empty(self):
        form_data = {"username": "",
                     "password1": "",
                     "password2": "",
                     "email": ""}
        form =  CustomUserCreationForm(form_data)

        self.assertFalse(form.is_valid())
    
    def test_all_fields_are_none(self):
        form_data = {"username": None,
                     "password1": None,
                     "password2": None,
                     "email": None}
        form =  CustomUserCreationForm(form_data)

        self.assertFalse(form.is_valid())
