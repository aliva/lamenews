from lamenews import models

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    error_messages = UserCreationForm.error_messages
    error_messages['duplicate_email'] = "a user with that email already exists"
    
    class Meta:
        model = get_user_model()
        fields = ("username", "email")
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
    
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = (
            'title',
            'content',
            'tags',
        )
        