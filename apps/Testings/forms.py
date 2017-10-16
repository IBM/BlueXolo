from django import forms

from .models import Collection
from apps.Products.models import Source


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'name',
            'description',
            'product',
        ]

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 3(products)"""
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Source.objects.filter(category=3)
