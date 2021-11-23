from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse
from django.db.models.query_utils import Q
from fapp.models import User


from fapp.models import Comment, DownVote, Post, UpVote

def createUser():
    """ A utility function to create a User """
    user = User.objects.create(username="nehe@gmail.com", password="1234")
    return user

def createPost():
    """
    A utility function to create a Post
    """
    user = createUser()
    body_text = "A new post"
    post = Post.objects.create(body=body_text, created_by=user)
    return post

class PostModelTests(TestCase):
    """ Tests for Post model """
    
    def test_create_post_with_all_fields(self):
        """ Creates a post with values given for default fields"""
        user = createUser()
        body_text = "Annother new post"
        post = Post.objects.create(body=body_text, created_by=user)

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


    def test_show_post(self):
        """
        A posts object should be present in template
        """
        response = self.client.get(reverse('fapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])

class VotingModelTests(TestCase):
    """Up_vote and down_vote tests"""

    def test_up_vote(self):
        """
        Should add an up_vote
        Only one should exist in db
        """
        post = createPost()
        user = post.created_by
        up_vote = UpVote.objects.create(voted_by=user, post=post)

        self.assertEqual(user, up_vote.voted_by)
        self.assertEqual(post, up_vote.post)

        up_votes = UpVote.objects.filter(Q(voted_by=user, post=post))
        self.assertTrue(len(up_votes), 1)

    
    def test_down_vote(self):
        """
        Should add a down_vote
        Only one should exist in db
        """
        post = createPost()
        user = post.created_by
        down_vote = DownVote.objects.create(down_voted_by=user, post=post)
        
        self.assertEqual(user, down_vote.down_voted_by)
        self.assertEqual(post, down_vote.post)

        down_votes = DownVote.objects.filter(Q(down_voted_by=user, post=post))
        self.assertTrue(len(down_votes), 1)
