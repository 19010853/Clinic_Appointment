from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


USER_TYPE = [
    ("Doctor", "Doctor"),
    ("Patient", "Patient"),
]

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
        required=True
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'johndoe@gmail.com'}),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'}),
        required=True
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE,
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email'].split('@')[0]
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'johndoe@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'}))

    class Meta:
        model = User
        fields = ['email', 'password']