from django import forms
from django.utils.safestring import mark_safe

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
            'category': mark_safe('Category Group <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Global Variables -> Variables that can be used under variables Profile  Local Network connection -> Variables that can be used under Connection profile">help_outline</i>')
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
