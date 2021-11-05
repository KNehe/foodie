from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import Post
from .forms import PostForm

def home(request):

    posts = Post.objects.all().order_by('-created_at')

    form = PostForm

    context = {'posts': posts, 'form': form}

    return render(request, "fapp/index.html",context)

def addpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data['foodie']
            Post.objects.create(body=data, created_by=request.user)
            return HttpResponseRedirect(reverse('fapp:home'))
        else:
            messages.error(request, "Fields are invalid")

    return HttpResponseRedirect(reverse('fapp:home'))
