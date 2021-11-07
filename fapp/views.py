from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import Post
from .forms import CustomUserCreationForm, PostForm

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
            # TODO send email
            return redirect(reverse('fapp:home'))
        messages.error(request, "\n".join([str(err) for err in form.error_messages.values()]))
        return redirect(reverse('fapp:register'))

    form = CustomUserCreationForm()
    
    context = {'form':form}

    return render(request, 'fapp/register.html', context)

def logout_user(request):
    logout(request)
    return redirect(reverse("fapp:home"))
