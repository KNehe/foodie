from functools import reduce
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError

from .models import Comment, DownVote, Post, UpVote
from .forms import CommentForm, CustomUserCreationForm, PostForm

import environ

env = environ.Env()

environ.Env.read_env()

def home(request):

    posts = Post.objects.all().order_by('-created_at')

    form = PostForm

    context = {'posts': posts, 'form': form}

    return render(request, "fapp/index.html",context)

@login_required(login_url='/login')
def addpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data['foodie']
            Post.objects.create(body=data, created_by=request.user)
            return redirect(reverse('fapp:home'))
        else:
            messages.error(request, "Fields are invalid")
            return redirect('fapp:home')

    return redirect(reverse('fapp:home'))

def login_user(request):
    
    if request.user.is_authenticated:
        return redirect(reverse('fapp:home'))

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('fapp:home'))
            else:
                messages.error(request, "Invalid username or password")
                return redirect(reverse('fapp:login'))
        else:
            messages.error(request, "Invalid username or password")
            return redirect(reverse('fapp:login'))
    
    form = AuthenticationForm()

    context = {'form':form}

    return render(request, 'fapp/login.html', context)

def register(request):
 
    if request.user.is_authenticated:
        return redirect(reverse('fapp:home'))

    if request.method == 'POST':
        form  = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            message = 'Thank you for joining us. \n We are excited to have you'
            from_email = env('FROM_EMAIL')
            send_mail('Foodie App Registration', message, from_email, [request.POST['email']], fail_silently=True)
            return redirect(reverse('fapp:home'))
        messages.error(request, "\n".join([str(err) for err in form.error_messages.values()]))
        return redirect(reverse('fapp:register'))

    form = CustomUserCreationForm()
    
    context = {'form':form}

    return render(request, 'fapp/register.html', context)

def logout_user(request):
    logout(request)
    return redirect(reverse("fapp:home"))

def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    message = render_to_string(email_template_name, c)
                    from_email = env('FROM_EMAIL')
                    try:
                        send_mail(subject, message, from_email, [user.email], fail_silently=True)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found')
                    except Exception as e:
                        print("Error sending email", e)
                        messages.error(request, 'An error occurred')
                        return redirect(reverse('fapp:password_reset'))

                    return redirect(reverse('fapp:password_reset_done'))


    password_reset_form = PasswordResetForm()

    context={"password_reset_form":password_reset_form}

    return render(request, 'password/password_reset.html', context)

@login_required(login_url='/login')
def up_vote(request, pk):
    """
    If user has already voted - remove vote
    If user has not voted - add vote
    Remove user's down_vote when adding up_vote
    Can't have up vote and down_vote at same time
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        messages.error(request, "Can't upvote for unknown post")
        return redirect(reverse("fapp:home"))
    
    up_vote = UpVote.objects.filter(Q(voted_by=request.user, post=post))
    if up_vote:
        up_vote.delete()
    else:
        down_vote = DownVote.objects.filter(Q(down_voted_by=request.user, post=post))
        if down_vote:
            down_vote.delete()
        UpVote.objects.create(post=post, voted_by=request.user)
    
    return redirect(reverse("fapp:home") + f"#{post.id}")


@login_required(login_url='/login')
def down_vote(request, pk):
    """
    If user has already down voted - remove down_vote
    If user has not down voted - add down_vote
    Remove user's up_vote when adding down_vote
    Can't have up vote and down_vote at same time
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        messages.error(request, "Can't upvote for unknown post")
        return redirect(reverse("fapp:home"))
    
    down_vote = DownVote.objects.filter(Q(down_voted_by=request.user, post=post))
    if down_vote:
        down_vote.delete()
    else:
        up_vote = UpVote.objects.filter(Q(post=post, voted_by=request.user))
        if up_vote:
            up_vote.delete()
        DownVote.objects.create(post=post, down_voted_by=request.user)
    
    return redirect(reverse('fapp:home') + f"#{post.id}")

@login_required(login_url='/login')
def comment(request, pk:str):
    
    post = Post.objects.filter(Q(pk=pk))
    if not post or len(post) == 0:
        messages.error(request, 'Post does not exist. No comments')
        return redirect(reverse('fapp:home'))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['comment']
            Comment.objects.create(body=data, created_by=request.user, post=post[0])
            return redirect(reverse('fapp:comments', kwargs={'pk': pk}))
        else:
            messages.error(request, 'Invalid comment')
            return redirect(reverse('fapp:home'))
    
    form = CommentForm()

    comments = Comment.objects.filter(Q(post=post[0])).order_by('-created_at')
    
    context = {'post': post, 'comments': comments, 'form': form}

    return render(request, 'fapp/comments.html', context)