from django import forms

from .models import ServerProfile


class ServerProfileForm(forms.ModelForm):
    class Meta:
        model = ServerProfile
        fields = [
            'name',
            'description',
            'template'
        ]
