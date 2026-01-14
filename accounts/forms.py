from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name","gender","location","birthday","summary","domain","field","website","github","linkedin","work","education","skills"]   # include your fields
