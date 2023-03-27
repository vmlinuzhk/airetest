from django import forms

from main.models import Bug, User


class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'owner', 'text']


class PersonForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']
