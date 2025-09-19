from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

UserNew = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserNew
        fields = ('username','email','password1','password2')
