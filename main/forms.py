from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field  # , Fieldset
from django import forms
from django.contrib import auth

from .models import Profile, User


class CustomField(Field):
    template = 'partials/inputs/custom-field.html'


class CustomSelect(Field):
    template = 'partials/inputs/custom-select.html'


class ProfileForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True, label='Password')
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Confirm Password', required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth', 'email']

    def __init__(self, *args, **kwargs):
        self.mode = 'edit' if kwargs.get('instance') is not None else 'create'
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.fields['email'].help_text = \
            'Ensure a valid accessible email is provided. Further communications will be ' \
            'through this email'
        # self.fields['username'].required = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        if self.mode == 'edit':
            self.fields['password1'].required = False
            self.fields['password2'].required = False

        self.helper.layout = Layout(
            Row(
                Div(CustomField('last_name'), css_class='form-group col'),
            ),
            Row(
                Div(CustomField('first_name'), css_class='form-group col'),
                Div(CustomField('middle_name'), css_class='form-group col'),
            ),
            Row(
                Div(CustomSelect('gender', ), css_class='form-group col'),
                Div(CustomField('date_of_birth'), css_class='form-group col'),
            ),
            Row(
                Div(CustomField('email'), css_class='form-group col'),
            ),
            Row(
                Div(CustomField('password1'), css_class='form-group col'),
                Div(CustomField('password2'), css_class='form-group col'),
            ),
        )

    def save(self, commit=True):
        obj = super().save(commit)
        if self.cleaned_data.get('password1', None).strip() != '':
            obj.set_password(self.cleaned_data['password1'])
        if commit:
            obj.save()
        return obj

    def clean(self):
        cleaned = super().clean()

        password = cleaned.get('password1')
        password2 = cleaned.get('password2')
        username = cleaned.get('email')
        email = cleaned.get('email')

        if password != '' and password2 != '' and password != password2:
            self.add_error('password1', 'Passwords do not match')
        if self.mode != 'edit':
            if User.objects.filter(email=email.lower()).exists():
                self.add_error('email', 'Email address already registered')
            if User.objects.filter(username=username.lower()).exists():
                self.add_error('email', 'Username is taken. Choose another')
            self.instance.username = username
        return cleaned


class LoginForm(forms.Form):
    email = forms.CharField(label='Username or Email address', required=True, )
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(self.request, user)
            else:
                self.add_error('password', 'Invalid username or password supplied')
        else:
            self.add_error('email', 'Username and/or password not given')
        return cleaned_data
