import re

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from uprofile.models import Seller, UProfile


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, help_text="Required. Only letters are allowed.")
    last_name = forms.CharField(max_length=50, required=True, help_text="Required. Only letters are allowed.")

    email = forms.EmailField(
        label="Email confirmation address",
        help_text="Please enter email address.",
        required=True,
    )

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

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise ValidationError('Email already in use.')
        return data

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]


class UProfileEditForm(forms.ModelForm):

    def save(self, commit=True):
        up = super().save(commit=False)
        up.profile_image.name = str(up.user.id) + "_" + up.profile_image.name
        if commit:
            up.save()
        return up



    class Meta:
        model = UProfile
        fields = ['profile_image']


class SellerApplyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'uprofile_post_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-success'))

    def clean_description(self, *args, **kwargs):
        description = self.cleaned_data.get('description')
        if len(description) == 0:
            raise forms.ValidationError('Description is required!')
        if len(description) < 75:
            raise forms.ValidationError(
                f'Description should contains at least 75 characters, but were {len(description)} given!')
        return description

    def clean_seller_name(self, *args, **kwargs):
        seller_name = self.cleaned_data.get('seller_name')
        if len(seller_name) == 0:
            raise forms.ValidationError('Name is required!')
        return seller_name

    def clean_legal_seller_address(self, *args, **kwargs):
        legal_seller_address = self.cleaned_data.get('legal_seller_address')
        if len(legal_seller_address) == 0:
            raise forms.ValidationError('Legal seller address is required!')

        special_puncs = ['!', '@', '#', '$', '%', '&', '*', '(', ')']
        for i in legal_seller_address:
            if i in special_puncs:
                raise ValidationError(
                    'Address cannot contains special chars.')

        return legal_seller_address

    class Meta:
        model = Seller
        fields = [
            'seller_name',
            'country',
            'legal_seller_address',
            'contact_phone',
            'seller_email',
            'description',
        ]

        labels = {
            'seller_name': "Please enter seller's business name.",
            'country': "Please provide a country name.",
            'legal_seller_address': 'Please enter legal address.',
            'contact_phone': 'Please enter contact phone number.',
            'seller_email': "Please enter seller's email.",
            'description': 'Please provide some useful information on what you will sell.',
        }
        help_texts = {
            'name': 'Some useful help text.',
        }
        error_messages = {
            'seller_name': {
                'max_length': "Seller name can not be empty or too long.",
            },
        }


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
