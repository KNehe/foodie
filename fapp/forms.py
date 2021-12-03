from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class PostForm(forms.Form):
    foodie = forms.CharField(label='',
                             max_length=200, 
                             widget=forms.Textarea(
                             attrs={'placeholder': 'Best meal to have today ?', 'rows': '4',
                                    'class':'input', 'style':'resize:none;'}))

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CommentForm(forms.Form):
    comment = forms.CharField(label='',
                               max_length=100,
                               widget=forms.Textarea(attrs={'placeholder': 'Add a comment',
                                                            'rows':'5',
                                                            'style':'resize:none;border-radius:8px;'}))

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['avatar','username', 'email', 'first_name', 'last_name']
