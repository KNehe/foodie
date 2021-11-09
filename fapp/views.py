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
                    try:
                        send_mail(subject, message, "kamolunehemiah@gmail.com", [user.email], fail_silently=False)
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
