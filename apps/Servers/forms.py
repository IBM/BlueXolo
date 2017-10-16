from django import forms

from .models import ServerProfile, JenkinsServerProfile


class ServerProfileForm(forms.ModelForm):
    class Meta:
        model = ServerProfile
        fields = [
            'name',
            'description',
            'template'
        ]


class NewJenkinsServerprofileForm(forms.ModelForm):
    class Meta:
        model = JenkinsServerProfile
        fields = '__all__'
