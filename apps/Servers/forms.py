from django import forms

from .models import ServerProfile, TemplateServer, Parameters


class ServerTemplateForm(forms.ModelForm):
    class Meta:
        model = TemplateServer
        fields = [
            'name',
            'category',
            'description'
        ]

        widgets = {
            "description": forms.Textarea(attrs={'class': 'materialize-textarea'})
        }


class ParametersForm(forms.ModelForm):
    class Meta:
        model = Parameters
        fields = [
            'category',
            'name',
            'help_text'
        ]

        labels = {
            'category': 'Category Group'
        }
        widgets = {
            'name': forms.TextInput(attrs={'id': 'param_name'}),
            'category': forms.Select(attrs={'id': 'category_group'})
        }


class ServerProfileForm(forms.ModelForm):
    class Meta:
        model = ServerProfile
        fields = [
            'name',
            'description',
            'template'
        ]

        widgets = {
            "description": forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
