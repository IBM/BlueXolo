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
        labels = {
            'name'         : mark_safe('Name <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Name to identify Template">help_outline</i>'),
            'category'     : mark_safe('Category Group <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Look the description for more information">help_outline</i>'),
            'description'  : mark_safe('Description <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Text to describe Template">help_outline</i>'),
        }
        
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
            'category'  : mark_safe('Category Group <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Look the description for more information">help_outline</i>'),
            'name'      : mark_safe('Name <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Name to identify the parameter">help_outline</i>'),
            'help_text' : mark_safe('Name <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Text that helps to identify the purpose of the parameter">help_outline</i>'),
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
        labels = {
            'name'         : mark_safe('Name <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Name to identify Profile">help_outline</i>'),
            'description'  : mark_safe('Description <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Text to describe Profile">help_outline</i>'),
            'template'     : mark_safe('Template <i style="float: right;" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Pick a created template">help_outline</i>'),
        }
        widgets = {
            "description": forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
