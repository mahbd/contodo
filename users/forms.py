# create registration form
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'todo_token', 'cf_handle',
                  'at_handle', 'lc_handle', 'tp_handle']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'todo_token', 'cf_handle', 'at_handle', 'lc_handle',
                  'tp_handle']
