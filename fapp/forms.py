from django import forms

class PostForm(forms.Form):
    foodie = forms.CharField(label='',
                             max_length=200, 
                             widget=forms.Textarea(attrs={'placeholder': 'Best meal to have today ?'}))