from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):

    first_name = forms.CharField(label="Имя", min_length=2)
    last_name = forms.CharField(label="Фамилия", min_length=2)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )
