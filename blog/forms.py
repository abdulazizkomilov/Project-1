from django import forms
from .models import User, Comment, Post
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, TextInput

class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.TextInput()
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) <= 2:
            raise forms.ValidationError("Username is too short")
        return username


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body','parent']
        widgets = {
            'body' : TextInput(),
        }
