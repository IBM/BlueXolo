from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, FormView
from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.permissions import available_perm_status

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
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['user_tasks'] = self.request.user.get_all_tasks()[:3]
        context['user_tasks2'] = self.request.user.get_all_tasks()[3:]
        return context

class StepperView(LoginRequiredMixin, TemplateView):
    template_name = "stepper.html"
    
    def get_context_data(self, **kwargs):
        context = super(StepperView, self).get_context_data(**kwargs)
        return context



class ArgumentsView(LoginRequiredMixin, HasPermissionsMixin, TemplateView):
    template_name = "arguments.html"
    required_permission = "read_argument"


class NewArgumentView(LoginRequiredMixin, HasPermissionsMixin, CreateView):
    model = Argument
    form_class = ArgumentForm
    template_name = "form-snippet.html"
    required_permission = "create_argument"

    def get_success_url(self):
        messages.success(self.request, "Argument Created")
        return reverse_lazy('commands')

    def get_context_data(self, **kwargs):
        cmd = Command.objects.get(id = self.kwargs.get('cmd'))
        form = self.form_class(cmd = cmd)
        context = super(NewArgumentView, self).get_context_data(**kwargs)
        context['title'] = "New Argument"
        context['form'] = form
        return context


class EditArgumentView(LoginRequiredMixin, HasPermissionsMixin, UpdateView):
    model = Argument
    form_class = ArgumentForm
    template_name = "form-snippet.html"
    required_permission = "update_argument"

    def get_success_url(self):
        messages.success(self.request, "Argument Edited")
        return reverse_lazy('commands')

    def get_context_data(self, **kwargs):
        context = super(EditArgumentView, self).get_context_data(**kwargs)
        context['title'] = "Edit Argument"
        context['delete'] = True
        return context

    def post(self, request, pk, *args, **kwargs):
        result = super(EditArgumentView, self).post(request, *args, **kwargs)
        instance = Argument.objects.get(pk = pk)
        include = request.POST.getlist('include[]')
        exclude = request.POST.getlist('exclude[]')
        instance.name = request.POST['name']
        instance.description = request.POST['description']
        instance.requirement = request.POST['requirement'].title()
        instance.needs_value = request.POST['needs_value'].title()
        instance.save()
        for i in instance.include.all():
            instance.include.remove(i)
        for e in instance.exclude.all():
            instance.exclude.remove(e)
        for i in include:
            instance.include.add(i)
            instance.save()
        for e in exclude:
            instance.exclude.add(e)
            instance.save()
        return result

class DeleteArgumentView(LoginRequiredMixin, HasPermissionsMixin, DeleteView):
    model = Argument
    template_name = "delete-argument.html"
    required_permission = "delete_argument"

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

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        can_create = False
        if user.is_superuser:
            can_create = True
        else:
            user_permissions = available_perm_status(user)
            permissions = [
                'create_robot',
                'create_libraries',
                'create_product'
            ]
            for perm in permissions:
                if perm in user_permissions and not can_create:
                    can_create = True
        if can_create:
            return super(CreateSourceView, self).dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "You don't have permission for this action")
            return HttpResponseRedirect(self.get_success_url())

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
        stepper = self.kwargs.get('stepper')
        _config = {}
        if name == 'products':
            form.instance.category = 3
            if Source.objects.filter(name=form.data.get('name'), version=form.data.get('version')):
                messages.warning(self.request, 'Already exist a Product with this name and version')
                return self.render_to_response(self.get_context_data(form=form))
            source = form.save()
            self.pk = source.pk
            if stepper != 'stepper':
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
            self.pk = source.pk
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
                if stepper != 'stepper':
                    messages.success(self.request, 'Robot Framework Source created')
        if name == 'libraries':
            form.instance.category = 5
            source = form.save()
            self.pk = source.pk
            _config = {
                'category': 5,
                'source': source.pk,
                'url': form.data.get('url')
            }
            file = form.files.get('html_file')
            if file:
                fs = FileSystemStorage(location = '{0}/zip/'.format(settings.MEDIA_ROOT))
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url('zip/{}'.format(filename))
                _config['url'] = self.request.build_absolute_uri('/' + uploaded_file_url)
            if stepper != 'stepper':
                messages.success(self.request, 'Library Source created')
        try:
            extract = run_extract.delay(_config)
            task = Task.objects.create(
                name="Extract commands from {0}".format(name),
                category=1,
                task_info="Started",
                task_id=extract.task_id,
                state=extract.state
            )
            if stepper != 'stepper':
                messages.info(self.request, 'Running extract in background')
            self.request.user.tasks.add(task)
            self.request.user.save()
            return HttpResponseRedirect(self.get_success_url())
        except Exception as error:
            messages.error(self.request, 'Error {0}'.format(error))
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        stepper = self.kwargs.get('stepper')
        if stepper != 'stepper':
            return reverse_lazy('source-list', kwargs={'slug': self.kwargs.get('slug')})
        else:
            source_pk = self.pk
            return reverse_lazy('successful', kwargs={'step': self.kwargs.get('slug'), 'pk': source_pk})

    def get_context_data(self, **kwargs):
        context = super(CreateSourceView, self).get_context_data()
        context['slug'] = self.kwargs.get('slug')
        context['title'] = 'New'
        context['extra'] = 'After press "Create" the system extract the commands for'
        context['stepper'] = self.kwargs.get('stepper')
        return context


class EditSourceView(LoginRequiredMixin, UpdateView):
    model = Source
    template_name = "create-edit-source.html"

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        can_create = False
        if user.is_superuser:
            can_create = True
        else:
            user_permissions = available_perm_status(user)
            permissions = [
                'update_robot',
                'update_libraries',
                'update_product'
            ]
            for perm in permissions:
                if perm in user_permissions and not can_create:
                    can_create = True
        if can_create:
            return super(EditSourceView, self).dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "You don't have permission for this action")
            return HttpResponseRedirect(self.get_success_url())

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
        source = form.save()
        self.pk = source.pk
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
        stepper = self.kwargs.get('stepper')
        if stepper != 'stepper':
            return reverse_lazy('source-list', kwargs={'slug': slug})
        else:
            source_pk = self.pk
            return reverse_lazy('successful', kwargs={'step': slug, 'pk': source_pk})

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
        context['stepper'] = self.kwargs.get('stepper')
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
            arguments = command.get_arguments()

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

    def get_context_data(self, **kwargs):
        context = super(CommandsView, self).get_context_data(**kwargs)
        context['stepper'] = self.kwargs.get('stepper')
        return context


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

    def form_valid(self, form):
        form.instance.user = self.request.user
        source = form.save()
        self.pk = source.pk
        return super(NewPhaseView, self).form_valid(form)

    #def get_success_url(self):
    #    messages.success(self.request, "Phase Created")
    #    return reverse_lazy('phases')
    
    def get_success_url(self):
        stepper = self.kwargs.get('stepper')
        source_pk = self.pk
        if stepper != 'stepper':
            messages.success(self.request, "Phase Created")
        if stepper != 'stepper':
            return reverse_lazy('phases')
        else:
            return reverse_lazy('successful', kwargs={'step': 'phases', 'pk': source_pk})

    def get_context_data(self, **kwargs):
        context = super(NewPhaseView, self).get_context_data(**kwargs)
        context['stepper'] = self.kwargs.get('stepper')
        return context

class EditPhaseView(LoginRequiredMixin, UpdateView):
    model = Phase
    form_class = PhaseForm
    template_name = 'create-edit-phase.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        source = form.save()
        self.pk = source.pk
        return super(EditPhaseView, self).form_valid(form)

    def get_success_url(self):
        stepper = self.kwargs.get('stepper')
        source_pk = self.pk
        if stepper != 'stepper':
            messages.success(self.request, "Phase Edited")
        if stepper != 'stepper':
            return reverse_lazy('phases')
        else:
            return reverse_lazy('successful', kwargs={'step': 'phases', 'pk': source_pk})
    
    def get_context_data(self, **kwargs):
        context = super(EditPhaseView, self).get_context_data(**kwargs)
        context['stepper'] = self.kwargs.get('stepper')
        return context

class DeletePhaseView(LoginRequiredMixin, DeleteView):
    model = Phase
    template_name = "delete-phase.html"

    def get_success_url(self):
        messages.success(self.request, "Phase deleted")
        return reverse_lazy('phases')


class SuccessfulView(LoginRequiredMixin, TemplateView):
    template_name = "successful.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessfulView, self).get_context_data(**kwargs)
        context['step'] = self.kwargs.get('step')
        context['pk'] = self.kwargs.get('pk')
        return context
