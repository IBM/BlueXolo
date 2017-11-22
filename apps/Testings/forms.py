from django import forms

from .models import Collection, Keyword
from apps.Products.models import Source


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'name',
            'description',
            'product',
        ]
        widgets = {
            'product': forms.Select(attrs={'required': True})
        }

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 3(products)"""
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Source.objects.filter(category=3)


class ImportScriptForm(forms.ModelForm):
    file_script = forms.FileField(forms.FileInput())

    class Meta:
        model = Keyword
        fields = [
            'name',
            'description',
            'file_script',
            'collection'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 3(products)"""
        super(ImportScriptForm, self).__init__(*args, **kwargs)
        self.fields['collection'].required = True


class EditImportScriptForm(forms.ModelForm):
    search_keyword = forms.CharField(widget=forms.TextInput(), required=False)

    class Meta:
        model = Keyword
        fields = [
            'name',
            'description',
            'collection',
            'script',
            'search_keyword'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'script': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }
