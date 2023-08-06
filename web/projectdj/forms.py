import re

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django import forms

from uprofile.models import UProfile


class MyUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        "email_missing": ("Please enter email."),
        "name_missing": ("Please enter name."),
    }

    first_name = forms.CharField(
        max_length=50,
        required=True,
        help_text="Required. Only letters are allowed.",
        widget=forms.TextInput(attrs={'placeholder': 'First name'}))

    last_name = forms.CharField(
        max_length=50,
        required=True,
        help_text="Required. Only letters are allowed.",
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    email = forms.EmailField(
        label="Email confirmation address",
        help_text="Please enter email address.",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Email address'}))

    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}),
                                help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        special_puncs = ['!', '@', '#', '$', '%', '&', '*', '(', ')']
        for i in first_name:
            if i in special_puncs:
                raise ValidationError(
                    'First name cannot contains special chars and punctuations.')
        if re.search(r'\d', first_name):
            raise ValidationError('First name must not have numbers')
        if re.search(r'\s', first_name):
            raise ValidationError('First name must not have spaces')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        special_puncs = ['!', '@', '#', '$', '%', '&', '*', '(', ')']
        for x in last_name:
            if x in special_puncs:
                raise ValidationError('Last name cannot contains special chars and punctuations.')

        if re.search(r'\d', last_name):
            raise ValidationError('Last name must not have numbers')
        if re.search(r'\s', last_name):
            raise ValidationError('Last name must not have spaces')
        return last_name

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            UProfile.objects.create(user=user, profile_image='')
            try:
                user.groups.add(Group.objects.get_or_create(name='normal')[0].id)
            except Group.DoesNotExist:
                pass

        return user
