from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from ushopping.models import Product


class SellerCreateProductForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'uprofile_post_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-success'))
    product_image = forms.FileField(required=True)

    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        if len(name) == 0:
            raise forms.ValidationError('Product name is required!')
        return name

    class Meta:
        model = Product
        fields = (
            'name',
            'publisher',
            'year',
            'condition',
            'author',
            'category',
            'short_description',
            'description',
            'product_image',
            'price',
        )

        labels = {
            'name': "Please enter product name.",
            'publisher': "Please enter publisher name of a product.",
            'author': "Please provide author name of a product",
            'category': 'Please enter category of a product',
            'short_description': 'Please provide a short description of a product.',
            'description': "Please provide full description of a product.",
            'price': 'Please enter price of a product.',
        }

        help_texts = {
            'name': 'Please enter product name.',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Endless Night.'}),
            'author': forms.TextInput(attrs={'placeholder': 'Agatha Christie'}),
            'publisher': forms.TextInput(attrs={'placeholder': 'Fontana'}),
            'short_description': forms.Textarea(attrs={'placeholder': 'Enter short description here'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter full description here'}),
        }