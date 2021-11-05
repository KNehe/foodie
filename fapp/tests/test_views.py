from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User


from fapp.models import Post
from fapp.views import addpost as addpost_view

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
