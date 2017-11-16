from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, FormView

from apps.Testings.models import Phase
from apps.Users.models import Task
from extracts import run_extract
from .models import Argument, Source, Command
from .forms import ArgumentForm, SourceProductForm, SourceRobotForm, SourceLibraryForm, SourceEditProductForm, \
    CommandForm, SourceEditLibraryForm, PhaseForm


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['PLATFORM_VERSION'] = settings.PLATFORM_VERSION
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['user_tasks'] = self.request.user.get_all_tasks()[:3]
        context['user_tasks2'] = self.request.user.get_all_tasks()[3:]
        return context


class ArgumentsView(LoginRequiredMixin, TemplateView):
    template_name = "arguments.html"


class NewArgumentView(LoginRequiredMixin, CreateView):
    model = Argument
    form_class = ArgumentForm
    template_name = "create-edit-argument.html"

    def get_success_url(self):
        messages.success(self.request, "Argument Created")
        return reverse_lazy('commands')

    def get_context_data(self, **kwargs):
        context = super(NewArgumentView, self).get_context_data(**kwargs)
        context['title'] = "New Argument"
        return context


class EditArgumentView(LoginRequiredMixin, UpdateView):
    model = Argument
    form_class = ArgumentForm
    template_name = "create-edit-argument.html"

    def get_success_url(self):
        messages.success(self.request, "Argument Edited")
        return reverse_lazy('commands')

    def get_context_data(self, **kwargs):
        context = super(EditArgumentView, self).get_context_data(**kwargs)
        context['title'] = "Edit Argument"
        context['delete'] = True
        return context


class DeleteArgumentView(LoginRequiredMixin, DeleteView):
    model = Argument
    template_name = "delete-argument.html"

    def get_success_url(self):
        messages.success(self.request, "Argument Deleted")
        return reverse_lazy('commands')


# - - - - - Sources - - - - - - - - -
class SourceList(LoginRequiredMixin, TemplateView):
    template_name = "source-list.html"

    def get_context_data(self, **kwargs):
        context = super(SourceList, self).get_context_data(**kwargs)
        name = kwargs.get('slug')
        if name:
            title = ''
            category = 0
            if name == 'products':
                title = 'Products'
                category = 3
            if name == 'robot':
                title = 'Robot Framework'
                category = 4
            if name == 'libraries':
                title = 'Robot Framework Libraries'
                category = 5
            context['title'] = title
            context['category'] = category
        return context


class CreateSourceView(LoginRequiredMixin, CreateView):
    model = Source
    template_name = "create-edit-source.html"

    def get_form_class(self):
        name = self.kwargs.get('slug')
        if name == 'products':
            return SourceProductForm
        if name == 'robot':
            return SourceRobotForm
        if name == 'libraries':
            return SourceLibraryForm

    def form_valid(self, form, **kwargs):
        name = self.kwargs.get('slug')
        _config = {}
        if name == 'products':
            form.instance.category = 3
            if Source.objects.filter(name=form.data.get('name'), version=form.data.get('version')):
                messages.warning(self.request, 'Already exist a Product with this name and version')
                return self.render_to_response(self.get_context_data(form=form))
            source = form.save()
            messages.success(self.request, 'Product {0} created'.format(source.name))
            host = form.data.get('host')
            if not host:
                return HttpResponseRedirect(self.get_success_url())
            if host:
                _config = {
                    'category': 3,
                    'source': source.pk,
                    'regex': form.data.get('regex'),
                    'path': form.data.get('path'),
                    'host': host,
                    'port': form.data.get('port'),
                    'username': form.data.get('username'),
                    'password': form.data.get('password')
                }
        if name == 'robot':
            form.instance.name = 'Robot Framework'
            form.instance.category = 4
            source = form.save()
            file = form.files.get('zip_file')
            if file:
                fs = FileSystemStorage(location='{0}/zip/'.format(settings.MEDIA_ROOT))
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url('zip/{}'.format(filename))
                _config = {
                    'category': 4,
                    'source': source.pk,
                    "zip": uploaded_file_url
                }
                messages.success(self.request, 'Robot Framework Source created')
        if name == 'libraries':
            form.instance.category = 5
            source = form.save()
            messages.success(self.request, 'Library Source created')
            _config = {
                'category': 5,
                'source': source.pk,
                'url': form.data.get('url')
            }
        try:
            extract = run_extract.delay(_config)
            task = Task.objects.create(
                name="Extract commands from {0}".format(name),
                category=1,
                task_info="Started",
                task_id=extract.task_id,
                state=extract.state
            )
            messages.info(self.request, 'Running extract in background')
            self.request.user.tasks.add(task)
            self.request.user.save()
            return HttpResponseRedirect(self.get_success_url())
        except Exception as error:
            messages.error(self.request, 'Error {0}'.format(error))
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('source-list', kwargs={'slug': self.kwargs.get('slug')})

    def get_context_data(self, **kwargs):
        context = super(CreateSourceView, self).get_context_data()
        context['slug'] = self.kwargs.get('slug')
        context['title'] = 'New'
        context['extra'] = 'After press "Create" the system extract the commands for'
        return context


class EditSourceView(LoginRequiredMixin, UpdateView):
    model = Source
    template_name = "create-edit-source.html"

    def get_form_class(self):
        _category = self.object.category
        if _category == 3:
            return SourceEditProductForm
        if _category == 4:
            return SourceRobotForm
        if _category == 5:
            return SourceEditLibraryForm

    def form_valid(self, form):
        name = self.kwargs.get('slug')
        if name == 'products':
            form.instance.category = 3
        if name == 'robot':
            form.instance.name = 'Robot Framework'
            form.instance.category = 4
        if name == 'libraries':
            form.instance.category = 5
        return super(EditSourceView, self).form_valid(form)

    def get_success_url(self):
        _category = self.object.category
        if _category == 3:
            slug = 'products'
        if _category == 4:
            slug = 'robot'
        if _category == 5:
            slug = 'libraries'
        return reverse_lazy('source-list', kwargs={'slug': slug})

    def get_context_data(self, **kwargs):
        context = super(EditSourceView, self).get_context_data()
        _category = self.object.category
        if _category == 3:
            slug = 'products'
        if _category == 4:
            slug = 'robot'
        if _category == 5:
            slug = 'libraries'
        context['slug'] = slug
        context['title'] = 'Edit'
        return context


class DeleteSourceView(LoginRequiredMixin, DeleteView):
    model = Source
    template_name = "delete-source.html"

    def get_success_url(self, slug):
        messages.success(self.request, 'Robot Framework Source and his commands deleted')
        return reverse_lazy('source-list', kwargs={'slug': slug})

    def delete(self, request, *args, **kwargs):
        source = self.get_object()
        slug = ''
        if source.category == 3:
            slug = 'products'
        if source.category == 4:
            slug = 'robot'
        if source.category == 5:
            slug = 'libraries'
        commands = Command.objects.filter(source=source.pk)
        for command in commands:
            arguments = command.arguments.all()

            if command.source.count() <= 1:
                command.delete()
        source.delete()
        return HttpResponseRedirect(self.get_success_url(slug))

    def get_context_data(self, **kwargs):
        context = super(DeleteSourceView, self).get_context_data()
        _category = self.object.category
        if _category == 3:
            slug = 'products'
        if _category == 4:
            slug = 'robot'
        if _category == 5:
            slug = 'libraries'
        context['slug'] = slug
        return context


class CommandsView(LoginRequiredMixin, TemplateView):
    template_name = "commands.html"


class NewCommandView(LoginRequiredMixin, FormView):
    model = Command
    template_name = 'create-edit-command.html'
    form_class = CommandForm

    def get_success_url(self):
        return reverse_lazy('commands')

    def get_context_data(self, **kwargs):
        context = super(NewCommandView, self).get_context_data(**kwargs)
        context['title'] = 'Create Command'
        context['ArgumentForm'] = ArgumentForm
        return context


class EditCommandView(LoginRequiredMixin, UpdateView):
    model = Command
    form_class = CommandForm
    template_name = 'create-edit-command.html'
    success_url = reverse_lazy('commands')

    def get_context_data(self, **kwargs):
        context = super(EditCommandView, self).get_context_data(**kwargs)
        context['title'] = 'Edit Command'
        context['ArgumentForm'] = ArgumentForm
        return context


class DeleteCommandView(LoginRequiredMixin, DeleteView):
    template_name = "delete-command.html"
    model = Command
    success_url = reverse_lazy("commands")


class PhasesView(LoginRequiredMixin, TemplateView):
    template_name = "phases.html"


class NewPhaseView(LoginRequiredMixin, CreateView):
    model = Phase
    form_class = PhaseForm
    template_name = 'create-edit-phase.html'

    def get_success_url(self):
        messages.success(self.request, "Phase Created")
        return reverse_lazy('phases')


class EditPhaseView(LoginRequiredMixin, UpdateView):
    model = Phase
    form_class = PhaseForm
    template_name = 'create-edit-phase.html'

    def get_success_url(self):
        messages.success(self.request, "Phase Edited")
        return reverse_lazy('phases')


class DeletePhaseView(LoginRequiredMixin, DeleteView):
    model = Phase
    template_name = "delete-phase.html"

    def get_success_url(self):
        messages.success(self.request, "Phase deleted")
        return reverse_lazy('phases')
