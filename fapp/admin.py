from django.contrib import admin

from .models import Comment, DownVote, Post, UpVote


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UpVote)
admin.site.register(DownVote)