from django.test import TestCase, RequestFactory
from django.urls import reverse
from fapp.models import User


from fapp.models import Post
from fapp.views import addpost as addpost_view, register as register_view, up_vote

# Home view tests
def createUser():
    """ A utility function to create a User """
    user = User.objects.create(username="nehe@gmail.com", password="1234")
    return user

class HomeViewTests(TestCase):

    def test_no_posts(self):
        """
        A posts object not should be present in template
        """
        response = self.client.get(reverse('fapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])
        self.assertContains(response, "No posts available")
    
    def test_show_post(self):
        """
        Should render posts in template
        """
        user = createUser()
        body_text = "A new post"
        post = Post.objects.create(body=body_text, created_by=user)
        response = self.client.get(reverse('fapp:home'))
        self.assertQuerysetEqual(response.context['posts'], [post])
        self.assertContains(response, post)
        self.assertEqual(response.status_code, 200)

class AddPostViewTests(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="john doe", password="secret")

    def test_add_post(self):
        """
        Should create a post and redirect to 'fapp:home'
        """
        request = self.factory.post(reverse('fapp:addpost'), data={'foodie': 'foodie'})
        request.user = self.user
        
        response = addpost_view(request)
        self.assertEqual(response.status_code, 302)

class RegisterUserViewTests(TestCase):

    def test_register_user_success(self):
        """
        Should create a user and redirect to 'fapp:home'
        """
        form_data = {"username": "nehe",
                     "password1": "ABCDe124",
                     "password2": "ABCDe124",
                     "email": "nehe@gmail.com"}

        response = self.client.post(reverse('fapp:register'), data=form_data)

        user = User.objects.get(email="nehe@gmail.com")
        
        self.assertEqual(user.username, "nehe")
        self.assertEqual(user.email, "nehe@gmail.com")
        self.assertRedirects(response, reverse('fapp:home'))
        self.assertEqual(response.status_code, 302)
    
    def test_show_register_page(self):
        """
        Should render the registration page
        when 'fapp:register' is hit with get request
        """

        response = self.client.get(reverse('fapp:register'))

        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, reverse("fapp:register"))

class LogoutUserViewTest(TestCase):
    def logout_user(self):
        """
        Should log out user
        """
        response = self.client.get(reverse('fapp:logout'))

        self.assertFalse(response.request.user)
        self.assertRedirects(response, reverse('fapp:home'), status_code=302)

class LoginUserViewTests(TestCase):


    def test_login_true(self):
        """
        Should login user
        """
        pass

class UpVoteTests(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="john doe", password="secret")
        self.post = Post.objects.create(body={"foodie": "foodie"}, created_by=self.user)
    
