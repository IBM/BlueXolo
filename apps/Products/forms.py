from django import forms

from apps.Testings.models import Phase
from .models import Argument, Source, Command


class ArgumentForm(forms.ModelForm):
    class Meta:
        model = Argument
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'data-length': 30, 'id': 'args_name'}),
            'description': forms.Textarea(attrs={'class': 'materialize-textarea',
                                                 'data-length': 70, 'id': 'args_description'})
        }


class PhaseForm(forms.ModelForm):
    class Meta:
        model = Phase
        fields = {
            'name',
            'product'
        }

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 4(Robot)"""
        super(PhaseForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Source.objects.filter(category=3)


class SourceProductForm(forms.ModelForm):
    path = forms.CharField(widget=forms.TextInput(), required=False)
    regex = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'class': 'materialize-textarea'}), required=False)
    host = forms.CharField(required=False)
    port = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Source
        fields = [
            'name',
            'version',
            'depends',
            'host',
            'port',
            'username',
            'password',
            'path',
            'regex',
        ]
        labels = {"name": "Product Name", "depends": "Dependence Requirement (Optional)"}

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 4(Robot)"""
        super(SourceProductForm, self).__init__(*args, **kwargs)
        self.fields['depends'].queryset = Source.objects.filter(category=4)
        self.fields[
            'regex'].initial = '( {2}-\w+, --\w+[ \\n=]| {2}-\w+[ \\n=]| {2}--\w+[ \\n=]| {2}--\w+-\w+[ \\n=]| {2}-\w+, --\w+-\w+[ \\n=])(?=[ <]*)'


class SourceEditProductForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = [
            'name',
            'version',
            'depends',
        ]
        labels = {"name": "Product Name", "depends": "Dependence Requirement (Optional)"}

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 4(Robot)"""
        super(SourceEditProductForm, self).__init__(*args, **kwargs)
        self.fields['depends'].queryset = Source.objects.filter(category=4)


class SourceRobotForm(forms.ModelForm):
    zip_file = forms.FileField(forms.FileInput())

    class Meta:
        model = Source
        fields = [
            'version',
            'zip_file'
        ]
        labels = {"version": "Robot Framework Version"}


class SourceLibraryForm(forms.ModelForm):
    url = forms.CharField(label='Documentation URL')

    class Meta:
        model = Source
        fields = [
            'name',
            'version',
            'url',
            'depends',
        ]
        labels = {"name": "Library Name", "depends": "Robot Version Requirement"}

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 4(Robot)"""
        super(SourceLibraryForm, self).__init__(*args, **kwargs)
        self.fields['depends'].queryset = Source.objects.filter(category=4)


class SourceEditLibraryForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = [
            'name',
            'version',
            'depends',
        ]
        labels = {"name": "Library Name", "depends": "Robot Version Requirement"}

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 4(Robot)"""
        super(SourceEditLibraryForm, self).__init__(*args, **kwargs)
        self.fields['depends'].queryset = Source.objects.filter(category=4)


class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = [
            'name',
            'source',
            'description',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'data-length': 30}),
            'description': forms.Textarea(attrs={'class': 'materialize-textarea', 'data-length': 70})
        }

    def __init__(self, *args, **kwargs):
        """ This filter exclude the control flow sentences """
        super(CommandForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = Source.objects.exclude(category=1)
        """ This Make required the source field """
        self.fields['source'].required = True
