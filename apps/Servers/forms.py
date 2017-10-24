from django import forms

from .models import ServerProfile, TemplateServer


class ServerTemplateForm(forms.ModelForm):
    class Meta:
        model = TemplateServer
        fields = [
            'name',
            'category',
            'description'
        ]


class ServerProfileForm(forms.ModelForm):
    class Meta:
        model = ServerProfile
        fields = [
            'name',
            'description',
            'template'
        ]
