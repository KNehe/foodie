from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.utils.timezone import datetime
from django.db.models import Count

from fapp.helpers import get_side_bars_data

from .models import Comment, DownVote, Post, UpVote, User
from .forms import CommentForm, CustomUserCreationForm, PostForm, ProfileForm

import environ
import re


env = environ.Env()

environ.Env.read_env()

def home(request):

    q = request.GET.get('search') if request.GET.get('search') != None else ''

    posts = Post.objects.filter(body__icontains=q).order_by('-created_at')
    
    popular, recent = get_side_bars_data(request)

    form = PostForm
    
    context = {'posts': posts, 'form': form, 'popular': popular, 'recent': recent}

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
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"auth{email, password}")
            user = authenticate(email=email, password=password)
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

    # Common code- found in down_vote(request,pk). Should be refactored
    referer = request.META['HTTP_REFERER']
    
    comment_search = re.search(r'/comments/post/', referer)
    
    if comment_search:
        return redirect(reverse('fapp:comments', kwargs={'pk': post.id }))
    
    profile_search = re.search(r'/profile/', referer)

    if profile_search:
        user_id = referer[-1:]
        return redirect(reverse('fapp:profile', kwargs={'pk':user_id}))

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
    
    # Common code- found in up_vote(request,pk). Should be refactored
    referer = request.META['HTTP_REFERER']
    
    comment_search = re.search(r'/comments/post/', referer)
    
    if comment_search:
        return redirect(reverse('fapp:comments', kwargs={'pk': post.id }))
    
    profile_search = re.search(r'/profile/', referer)

    if profile_search:
        user_id = referer[-1:]
        return redirect(reverse('fapp:profile', kwargs={'pk':user_id}))
    
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
    
    popular, recent = get_side_bars_data(request)

    
    form = CommentForm()

    comments = Comment.objects.filter(Q(post=post[0])).order_by('-created_at')
    
    context = {'post': post, 'comments': comments, 'form': form, 'popular': popular, 'recent': recent}

    return render(request, 'fapp/comments.html', context)

def show_user_profile(request, pk):        

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            messages.error(request, 'User unknown')
            return redirect(reverse('fapp:home'))
        
        posts = Post.objects.filter(Q(created_by=user))

        popular, recent = get_side_bars_data(request)

        context = {'user': user, 'posts': posts, 'popular': popular, 'recent':recent}
        
        return render(request, 'fapp/profile.html', context)
    
@login_required(login_url='login')
def edit_profile(request, pk):
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated !')
            return redirect(reverse('fapp:edit_profile', kwargs={'pk':request.user.id}))
        
        messages.error(request, 'Invalid data found in form')
        return redirect(reverse('fapp:edit_profile', kwargs={'pk':request.user.id}))
    try:
        user = User.objects.get(pk=pk)
    except Post.DoesNotExist:
       return HttpResponse('You do not have access')
    
    form = ProfileForm(instance=user)

    context = {'form': form}

    return render(request, 'fapp/edit_profile.html', context)


@login_required(login_url='login')
def delete_account(request, pk):
    
    user = User.objects.filter(id=pk)
    
    logout(request)

    user.delete()

    return redirect(reverse('fapp:home'))

@login_required(login_url='login')
def delete_post(request, pk):
    post = Post.objects.filter(Q(id=pk))
    if post:
        post.delete()
    
    return redirect(reverse('fapp:home'))

def delete_comment(request, pk):
    comment = Comment.objects.filter(Q(id=pk))
    if comment:
        comment.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))