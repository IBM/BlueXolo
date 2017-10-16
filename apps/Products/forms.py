from django import forms

from .models import Argument, Source, Command


class ArgumentForm(forms.ModelForm):
    class Meta:
        model = Argument
        fields = '__all__'


class SourceProductForm(forms.ModelForm):
    path = forms.CharField(widget=forms.TextInput())
    regex = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'class': 'materialize-textarea'}), required=False)
    host = forms.CharField()
    port = forms.IntegerField()
    username = forms.CharField()

    password = forms.CharField(widget=forms.PasswordInput())

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
            'description',
            'source'
        ]

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 4(Robot)"""
        super(CommandForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = Source.objects.exclude(category=1)
