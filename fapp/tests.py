from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from .models import Comment, Post

def createUser():
    """ A utility function to create a User """
    user = User.objects.create(username="nehe@gmail.com", password="1234")
    return user

class PostModelTests(TestCase):
    """ Tests for Post model """
    def test_create_a_post_with_default_field(self):
        """
        Creates a post with body and user
        Default fields(up_vote and down_vote) should be created
        """
        user = createUser()
        body_text = "A new post"
        post = Post.objects.create(body=body_text, created_by=user)

        self.assertEqual(post.body, body_text)
        self.assertEqual(post.created_by, user)
        self.assertEqual(post.up_vote, 0)
        self.assertEqual(post.down_vote, 0)
        self.assertTrue(post.created_at)
    
    def test_create_post_with_all_fields(self):
        """ Creates a post with values given for default fields"""
        user = createUser()
        body_text = "Annother new post"
        post = Post.objects.create(body=body_text, created_by=user, up_vote=2, down_vote=1)

        self.assertEqual(post.up_vote, 2)
        self.assertEqual(post.down_vote, 1)
        self.assertEqual(post.body, body_text)
        self.assertEqual(post.created_by, user)
    
    def test_attempt_create_test_with_no_body(self):
        """ Should raise an error when body is None"""
        user = createUser()

        with self.assertRaises(IntegrityError):
                Post.objects.create(body=None, created_by=user)
    
    def test_attempt_create_test_with_no_user(self):
        """Should raise an error when User is not given"""
        with self.assertRaises(IntegrityError):
            Post.objects.create(body="Body")
    
    def test_unknown_parameter(self):
        """ Should raise a type error for unknown arg"""
        with self.assertRaises(TypeError):
            Post.objects.create(fake_field="fake arg", body="body", create_by= createUser())

class CommentModelTests(TestCase):
    """ Tests for Comment model """

    def test_create_comment(self):
        """
        Creates a comment for a particular post
        """
        user = createUser()
        body_text = "A new post"
        post = Post.objects.create(body=body_text, created_by=user)
        
        comment = Comment.objects.create(body=body_text, created_by=user, post=post)

        self.assertEqual(comment.post, post)
        self.assertEqual(comment.body, body_text)
        self.assertEqual(comment.created_by, user)
    
    def test_body_not_exist(self):
        """
        Should raise an error when Comment body is None
        """
        with self.assertRaises(IntegrityError):
            user = createUser()
            body_text = "A new post"
            post = Post.objects.create(body=body_text, created_by=user)
            Comment.objects.create(body=None, created_by=user, post=post)

