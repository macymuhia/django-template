from django import forms
from src.departments.models import *


class DepartmentCreationForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['name', 'description']


class EditDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
