from django import forms

from .models import Collection, Keyword, Phase, Collection
from apps.Products.models import Source

SCRIPT_TYPE_CHOICES = (
    (None, 'Choose a script type'),
    ('kw', 'Keyword'),
    ('tc', 'Test case'),
    ('ts', 'Test suite'),
)


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'name',
            'description',
            'product',
        ]
        widgets = {
            'product': forms.Select(attrs={'required': True}),
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 3(products)"""
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Source.objects.filter(category=3)


class NewImportScriptForm(forms.Form):
    script_type = forms.CharField(widget=forms.Select(choices=SCRIPT_TYPE_CHOICES))
    collection = forms.ModelChoiceField(queryset=Collection.objects.all())
    phase = forms.ModelChoiceField(queryset=Phase.objects.all())
    name = forms.CharField(max_length=100)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)
    file_script = forms.FileField()


class EditImportScriptForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = [
            'name',
            'description',
            'script',

        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'script': forms.Textarea(attrs={
                'class': 'materialize-textarea',
                'spellcheck': 'false',
                'style': 'max-height: 25vh; overflow: scroll'
            })
        }
