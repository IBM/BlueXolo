from django import forms

from apps.Testings.models import Phase
from .models import Argument, Source, Command
from django.utils.safestring import mark_safe

class ArgumentForm(forms.ModelForm):
    class Meta:
        model = Argument
        fields = '__all__'
        widgets = {
            'command' : forms.HiddenInput(),
            'name': forms.TextInput(attrs={'data-length': 30, 'id': 'args_name'}),
            'description': forms.Textarea(attrs={'class': 'materialize-textarea',
                                                 'data-length': 70, 'id': 'args_description'}),
        }

    def __init__(self, *args, **kwargs):
        cmd = None
        try:
            cmd = kwargs.pop('cmd')
        except KeyError:
            pass
        super(ArgumentForm, self).__init__(*args, **kwargs)
        if cmd:
            self.initial["command"] = cmd.id
            self.fields['include'].queryset = Argument.objects.filter(command=cmd)
            self.fields['exclude'].queryset = Argument.objects.filter(command=cmd)
        try:
            if self.instance:
                self.fields['include'].queryset = Argument.objects.filter(command=self.instance.command).exclude(id = self.instance.id)
                self.fields['exclude'].queryset = Argument.objects.filter(command=self.instance.command).exclude(id = self.instance.id)
            else:
                self.initial["command"] = cmd.id
        except:
            pass


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
    zip_file = forms.FileField()

    class Meta:
        model = Source
        fields = [
            'version',
            'zip_file'
        ]
        labels = {"version": "Robot Framework Version"}


class SourceLibraryForm(forms.ModelForm):
    url = forms.CharField(label='Documentation URL or file', required=False)
    html_file = forms.FileField(label='HTML File', required=False)
    class Meta:
        model = Source
        fields = [
            'name',
            'version',
            'url',
            'html_file',
            'depends',
        ]
        labels = {"name": "Library Name", "depends": "Robot Version Requirement"}

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url').strip()
        html_file = cleaned_data.get('html_file')
        page_name = "http://robotframework.org"
        html_name = ".html"
        head_url = url[:25]
        tail_url = url[-5:]

        #print ("Head URL: ")
        #print (head_url)
        #print ("Tail URL: ")
        #print (tail_url)

        if html_file is None and (url is None or url == ''):
            msg = "Please enter either the library's URL or HTML file."
            self.add_error('url', msg)
        else:
            if page_name != head_url:
                msg = "Please enter a valid url from Robot Framework"
                self.add_error('url',msg)
            else:     
                if html_name != tail_url:
                    msg = "Please enter a valid .html page from Robot Framework"
                    self.add_error('url',msg)




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

        labels = {
            "name"        : mark_safe('<b>Command <i style="float: right" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Provide the command that will be used in the product">help_outline</i></b>'),
            "source"      : mark_safe('<b>Source <i style="float: right" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Select the product associated with the new command">help_outline</i></b>'),
            "description" : mark_safe('<b>Description <i style="float: right" class="tiny material-icons tooltipped" data-position="bottom" data-tooltip="Provide a brief description about the command">help_outline</i></b>'),
        }

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
