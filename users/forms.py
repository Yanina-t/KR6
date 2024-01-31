from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from mailing_app.forms import StyleFormMixin
from users.models import User
from django import forms


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
