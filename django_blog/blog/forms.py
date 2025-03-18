from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Post, Comment
from taggit.forms import TagWidget



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'password': 'Password',
        }

        help_texts = {  
            'username': '',
        }

        widgets = {

            'username': forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control mb-4'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control mb-4'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control mb-4'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Valid Email','class': 'form-control mb-4'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Strong Password','class': 'form-control mb-4'}),
        }


class PostForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ["title", "content", "published_date", "author"]
        labels = {
            'title': 'title',
            'content': 'content',
            'published_date': 'published_date',
            'author': 'Author',
            'tags': 'tags',
        }


        widgets = {

            'title': forms.TextInput(attrs={'placeholder': 'title','class': 'form-control mb-4'}),
            'content': forms.TextInput(attrs={'placeholder': 'content','class': 'form-control mb-4'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control mb-4'}),
            'author': forms.CharField(attrs={'placeholder': 'author','class': 'form-control mb-4'}),
            'tags': TagWidget(),
        }




class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["post", "author", "content", "created_at", "updated_at"]
        labels = {
            'content': 'content',
        }

        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'content','class': 'form-control mb-4'}),
        }
