from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    body = models.TextField(max_length=200)
    up_vote = models.PositiveBigIntegerField(default=0)
    down_vote = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.body

class Comment(models.Model):
    body = models.TextField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.body