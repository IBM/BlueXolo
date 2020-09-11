import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView, DetailView
from django.core.files import File
from django.db import connection
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from rolepermissions.mixins import HasPermissionsMixin

from apps.Testings.models import Keyword, Collection, TestCase, TestSuite
from apps.Testings.forms import CollectionForm, ImportScriptForm, EditImportScriptForm
from json import *

class KeyWordsView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "keywords.html"
    required_permission = "read_keyword"


class NewKeywordView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "create-keyword.html"
    required_permission = "create_keyword"

    def get_context_data(self, **kwargs):
        context = super(NewKeywordView, self).get_context_data(**kwargs)
        context['stepper'] = self.kwargs.get('stepper')
        return context


class EditKeywordView(LoginRequiredMixin, HasPermissionsMixin, DetailView):
    model = Keyword
    template_name = "edit-keyword.html"
    required_permission = "update_keyword"

    def get_context_data(self, **kwargs):
        context = super(EditKeywordView, self).get_context_data(**kwargs)
        context['stepper'] = self.kwargs.get('stepper')
        return context

class DownloadKeywordView(LoginRequiredMixin,HasPermissionsMixin, TemplateView):
    model=Keyword
    template_name="download-keyword.html"
    required_permission="download_keyword"
    responseData={}
    def get_context_data(self, **kwargs):
        context = super(DownloadKeywordView, self).get_context_data(**kwargs)
        keywordId=kwargs['pk']
        return context;
    def dispatch(self, request, *args, **kwargs):
        responseData={}
        keywordId=kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM keywords where id=%s',[kwargs['pk']])
            row = cursor.fetchone()
        keywordName=row[1]
        keywordDesc=row[2]
        keywordScript=row[3]
        responseData['Name']=keywordName
        responseData['Script']=keywordScript
        responseData['Description']=keywordDesc
        return render(request,'download-keyword.html',{'data':responseData})


class DeleteKeywordView(LoginRequiredMixin, HasPermissionsMixin, DeleteView):
    template_name = "delete-keyword.html"
    model = Keyword
    required_permission = "delete_keyword"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user or request.user.is_staff:
            return super(DeleteKeywordView, self).dispatch(request, *args, **kwargs)
        elif obj.user != request.user:
            messages.warning(request, "You don't have permission for this action")
            return redirect('keywords')

    def get_success_url(self):
        messages.success(self.request, "Keyword Deleted")
        return reverse_lazy('keywords')


class TestCaseView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "testcases.html"
    required_permission = "read_test_case"


class NewTestCaseView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "create-testcase.html"
    required_permission = "create_test_case"

    def get_context_data(self, **kwargs):
        context = super(NewTestCaseView, self).get_context_data(**kwargs)
        context['stepper'] = self.kwargs.get('stepper')
        return context


class EditTestCaseView(LoginRequiredMixin, HasPermissionsMixin, DetailView):
    model = TestCase
    template_name = "edit-testcase.html"
    required_permission = "update_test_case"

    def get_context_data(self, **kwargs):
        context = super(EditTestCaseView, self).get_context_data(**kwargs)
        context['stepper'] = self.kwargs.get('stepper')
        return context

class DownloadTestcaseView(LoginRequiredMixin,HasPermissionsMixin, TemplateView):
    model=TestCase
    template_name="download-testcase.html"
    required_permission="download_test_case"
    responseData={}
    def get_context_data(self, **kwargs):
        context = super(DownloadTestcaseView, self).get_context_data(**kwargs)
        keywordId=kwargs['pk']
        return context;
    def dispatch(self, request, *args, **kwargs):
        responseData={}
        testCaseId=kwargs['pk']
        testCaseDependencies={}
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM testcases where id=%s',[kwargs['pk']])
            row = cursor.fetchone()
        subId=row[0]
        testCaseName=row[1]
        testCaseDesc=row[2]
        testCaseContent=row[3]
        KeywordsDict = json.loads(row[10])
        elements = KeywordsDict.get('keywords')
        if elements:
            for k in elements:
                current_pk = k.get('id')
                current_script = str(k.get('script'))
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM keywords where id=%s',(current_pk))
                    row = cursor.fetchone()
                keywordname = str(row[1])
                testCaseDependencies[keywordname]=current_script
        responseData['Name']=testCaseName
        responseData['Script']=testCaseContent
        responseData['Description']=testCaseDesc
        responseData['Dependencies']= json.dumps(testCaseDependencies)
        return render(request,'download-testcase.html',{'data':responseData})

class DeleteTestCaseView(LoginRequiredMixin, HasPermissionsMixin, DeleteView):
    template_name = "delete-testcase.html"
    model = TestCase

    required_permission = "delete_test_case"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user or request.user.is_staff:
            return super(DeleteTestCaseView, self).dispatch(request, *args, **kwargs)
        elif obj.user != request.user:
            messages.warning(request, "You don't have permission for this action")
            return redirect('testcases')

    def get_success_url(self):
        messages.success(self.request, "Test Case Deleted")
        return reverse_lazy('testcases')


class TestSuiteView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "testsuites.html"
    required_permission = "read_test_suite"


class NewTestSuiteView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "create-testsuites.html"
    required_permission = "create_test_suite"

    def get_context_data(self, **kwargs):
        context = super(NewTestSuiteView, self).get_context_data(**kwargs)
        context['stepper'] = self.kwargs.get('stepper')
        return context


class EditTestSuiteView(LoginRequiredMixin, HasPermissionsMixin, DetailView):
    model = TestSuite
    template_name = "edit-testsuites.html"
    required_permission = "update_test_suite"

    def get_context_data(self, **kwargs):
        context = super(EditTestSuiteView, self).get_context_data(**kwargs)
        context['stepper'] = self.kwargs.get('stepper')
        return context

class DownloadTestSuiteView(LoginRequiredMixin,HasPermissionsMixin,DetailView):
    model=TestSuite
    template_name="download-testsuites.html"
    required_permission="download_test_suite"
    responseData={}
    def get_context_data(self, **kwargs):
        context = super(DownloadTestSuiteView, self).get_context_data(**kwargs)
        keywordId=kwargs['pk']
        return context;
    def dispatch(self, request, *args, **kwargs):
        responseData={}
        testCaseId=kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM testsuites where id=%s',[kwargs['pk']])
            row = cursor.fetchone()
        subId=row[0]
        testSuiteName=row[1]
        testSuiteDesc=row[2]
        testSuiteContent=row[3]
        testSuiteDependenciesList=row[8]
        responseData['Name']=testSuiteName
        responseData['Script']=testSuiteContent
        responseData['Description']=testSuiteDesc
        responseData['Dependencies']=testSuiteDependenciesList
        print(testSuiteDependenciesList)
        return render(request,'download-testsuite.html',{'data':responseData})


class DeleteTestSuiteView(LoginRequiredMixin, HasPermissionsMixin, DeleteView):
    template_name = "delete-testsuite.html"
    model = TestSuite

    required_permission = "delete_test_suite"

    def get_success_url(self):
        messages.success(self.request, "Test Suite Deleted")
        return reverse_lazy("testsuites")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user or request.user.is_staff:
            return super(DeleteTestSuiteView, self).dispatch(request, *args, **kwargs)
        elif obj.user != request.user:
            messages.warning(request, "You don't have permission for this action")
            return redirect('testsuites')


class CollectionsView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "collections.html"
    required_permission = "read_collection"


class NewCollectionsView(LoginRequiredMixin, HasPermissionsMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = "create-edit-collection.html"
    required_permission = "create_collection"

    def form_valid(self, form):
        form.instance.user = self.request.user
        source = form.save()
        self.pk = source.pk
        return super(NewCollectionsView, self).form_valid(form)

    def get_success_url(self):
        stepper = self.kwargs.get('stepper')
        source_pk = self.pk
        if stepper != 'stepper':
            messages.success(self.request, "Collection Created")
        if stepper != 'stepper':
            return reverse_lazy('collections')
        else:
            return reverse_lazy('successful', kwargs={'step': 'collections', 'pk': source_pk})

    def get_context_data(self, **kwargs):
        context = super(NewCollectionsView, self).get_context_data(**kwargs)
        context['title'] = "New Collection"
        context['stepper'] = self.kwargs.get('stepper')
        return context


class EditCollectionsView(LoginRequiredMixin, HasPermissionsMixin, UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = "create-edit-collection.html"
    required_permission = "update_collection"

    def form_valid(self, form):
        form.instance.user = self.request.user
        source = form.save()
        self.pk = source.pk
        return super(EditCollectionsView, self).form_valid(form)

    def get_success_url(self):
        stepper = self.kwargs.get('stepper')
        source_pk = self.pk
        if stepper != 'stepper':
            messages.success(self.request, "Collection Edited")
        if stepper != 'stepper':
            return reverse_lazy('collections')
        else:
            return reverse_lazy('successful', kwargs={'step': 'collections', 'pk': source_pk})


    def get_context_data(self, **kwargs):
        context = super(EditCollectionsView, self).get_context_data(**kwargs)
        context['title'] = "Edit Collections"
        context['stepper'] = self.kwargs.get('stepper')
        return context


class DeleteCollectionsView(LoginRequiredMixin, HasPermissionsMixin, DeleteView):
    model = Collection
    template_name = "delete-collections.html"
    required_permission = "delete_collection"

    def get_success_url(self):
        messages.success(self.request, "Collection Deleted")
        return reverse_lazy('collections')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user or request.user.is_staff:
            return super(DeleteCollectionsView, self).dispatch(request, *args, **kwargs)
        elif obj.user != request.user:
            messages.warning(request, "You don't have permission for this action")
            return redirect('collections')


class KeywordsImportedView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "list-import-script.html"
    required_permission = "read_imported_script"


class NewKeywordImportedView(LoginRequiredMixin, HasPermissionsMixin, CreateView):
    template_name = "import-script.html"
    form_class = ImportScriptForm
    model = Keyword
    required_permission = "create_imported_script"

    def form_valid(self, form):
        file = form.files.get('file_script')
        if file:
            try:
                file_content = file.read()
                form.instance.script = file_content
                form.instance.user = self.request.user
                form.instance.script_type = 2
                form.save()
            except Exception as error:
                print(error)
        messages.success(self.request, "Script imported")
        return super(NewKeywordImportedView, self).form_valid(form)

    def form_invalid(self, form):
        return super(NewKeywordImportedView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('edit-import-script', kwargs={'pk': self.object.pk})


class EditKeywordImportedView(LoginRequiredMixin, HasPermissionsMixin, UpdateView):
    form_class = EditImportScriptForm
    template_name = "edit-import-script.html"
    model = Keyword
    required_permission = "update_imported_script"

    def form_invalid(self, form):
        return super(EditKeywordImportedView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "Script updated")
        return reverse_lazy('edit-import-script', kwargs={'pk': self.object.pk})


class DeleteImportedScriptView(LoginRequiredMixin, HasPermissionsMixin, DeleteView):
    model = Keyword
    template_name = 'delete-imported-script.html'
    required_permission = "delete_imported_script"

    def get_success_url(self):
        messages.success(self.request, "Script deleted")
        return reverse_lazy('imported-scripts')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user or request.user.is_staff:
            return super(DeleteImportedScriptView, self).dispatch(request, *args, **kwargs)
        elif obj.user != request.user:
            messages.warning(request, "You don't have permission for this action")
            return redirect('imported-scripts')


def apply_highlight(script):
    """This function use a pygments library for make a html highlight element. """
    if script:
        try:
            lexer = get_lexer_by_name("robotframework", stripall=True)
            formatter = HtmlFormatter(linenos=False, cssclass="source")
            with_highlight = highlight(script, lexer, formatter)
            return with_highlight
        except Exception as error:
            print(error)


class RunScriptView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "run_script.html"

    required_permission = "run_scripts"

    def get_context_data(self, **kwargs):
        context = super(RunScriptView, self).get_context_data(**kwargs)
        type_script = int(kwargs.get('type_script'))
        scripts = ['Keyword', 'Test Case', 'Test Suite']
        if type_script:
            if type_script == 1:
                obj = Keyword.objects.get(pk=kwargs.get('pk'))
            if type_script == 2:
                obj = TestCase.objects.get(pk=kwargs.get('pk'))
            if type_script == 3:
                obj = TestSuite.objects.get(pk=kwargs.get('pk'))
            context['obj'] = obj
            context['type'] = scripts[type_script - 1]
            context['type_id'] = type_script
            context['script'] = apply_highlight(obj.script)
            context['stepper'] = self.kwargs.get('stepper')
        return context
