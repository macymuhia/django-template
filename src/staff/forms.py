from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

from src.staff.models import *


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', "email"]


class UserSetPasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']


class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['group', 'role', 'department']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["photo", 'phone', 'bio']


class CustomGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(),
                                                 widget=forms.CheckboxSelectMultiple(), required=True)

    class Meta:
        model = CustomGroup
        fields = [
            'name',
            'permissions',
        ]
