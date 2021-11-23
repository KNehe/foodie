from django.contrib import admin

from .models import Comment, DownVote, Post, UpVote, User


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UpVote)
admin.site.register(DownVote)
admin.site.register(User)