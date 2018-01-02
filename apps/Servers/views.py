import json
import paramiko
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from random import choice
from scp import SCPClient
from string import ascii_lowercase, digits

from apps.Products.models import Source
from apps.Testings.models import Keyword, TestCase, TestSuite
from .forms import ServerProfileForm, ServerTemplateForm, ParametersForm
from .models import TemplateServer, ServerProfile, Parameters

from celery import shared_task


class ServerTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "servers-templates.html"


class NewServerTemplate(LoginRequiredMixin, CreateView):
    template_name = "create-server-template.html"
    model = TemplateServer
    success_url = reverse_lazy('servers-templates')
    form_class = ServerTemplateForm

    def get_context_data(self, **kwargs):
        context = super(NewServerTemplate, self).get_context_data(**kwargs)
        context['ParametersForm'] = ParametersForm
        return context


class EditServerTemplate(LoginRequiredMixin, UpdateView):
    model = TemplateServer
    template_name = "edit-server-template.html"
    success_url = reverse_lazy('servers-templates')
    form_class = ServerTemplateForm

    def get_context_data(self, **kwargs):
        context = super(EditServerTemplate, self).get_context_data(**kwargs)
        context['ParametersForm'] = ParametersForm
        return context


class DeleteServerTemplate(LoginRequiredMixin, DeleteView):
    model = TemplateServer
    template_name = "delete-template.html"

    def get_success_url(self):
        messages.success(self.request, "Template Deleted")
        return reverse_lazy('servers-templates')


class ServerProfileView(LoginRequiredMixin, TemplateView):
    template_name = "server-profiles.html"


class NewServerProfileView(LoginRequiredMixin, CreateView):
    template_name = "create-server-profile.html"
    success_url = reverse_lazy('servers-profiles')
    form_class = ServerProfileForm


class EditServerProfileView(LoginRequiredMixin, UpdateView):
    template_name = "edit-server-profile.html"
    success_url = reverse_lazy('servers-profiles')
    form_class = ServerProfileForm
    model = ServerProfile


class DeleteServerProfile(LoginRequiredMixin, DeleteView):
    model = ServerProfile
    template_name = "delete-profile.html"

    def get_success_url(self):
        messages.success(self.request, "Profile Deleted")
        return reverse_lazy('servers-profiles')


class ParametersView(LoginRequiredMixin, TemplateView):
    template_name = "parameters.html"


class NewParametersView(LoginRequiredMixin, CreateView):
    template_name = 'create-edit-parameter.html'
    success_url = reverse_lazy('parameters')
    form_class = ParametersForm

    def get_success_url(self):
        messages.success(self.request, "Parameter Created")
        return reverse_lazy('parameters')

    def get_context_data(self, **kwargs):
        context = super(NewParametersView, self).get_context_data(**kwargs)
        context['title'] = 'Create Parameter'
        return context


class EditParametersView(LoginRequiredMixin, UpdateView):
    template_name = "create-edit-parameter.html"
    success_url = reverse_lazy("parameters")
    form_class = ParametersForm
    model = Parameters

    def get_success_url(self):
        messages.success(self.request, "Parameter Edited")
        return reverse_lazy('parameters')

    def get_context_data(self, **kwargs):
        context = super(EditParametersView, self).get_context_data(**kwargs)
        context['title'] = 'Edit Parameter'
        return context


class DeleteParametersView(LoginRequiredMixin, DeleteView):
    model = Parameters
    template_name = "delete-parameters.html"

    def get_success_url(self):
        messages.success(self.request, "Parameter Deleted")
        return reverse_lazy('parameters')


# - - - - - - - - - Run on Server functions - - - - - - - - - - -

def get_config_object(params):
    """get config object for connection"""
    data_result = dict()
    for var in params:
        try:
            param = Parameters.objects.get(pk=var.get('id'))
            data_result['{0}'.format(param.name)] = var.get('value')
        except Exception as error:
            data_result['text'] = '{0}'.format(error)
    return data_result


def get_connection(config):
    """Create a paramiko connection for ssh communication"""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _port = 22
        if config.get('port'):
            _port = int(config.get('port'))
        client.connect(
            config.get('host'),
            username=config.get('user'),
            password=config.get('passwd'),
            port=_port)
    except Exception as error:
        client = error
    return client


def generate_filename(_script):
    """Generate a string like NAME_w0ln0t"""
    name = _script.replace(" ", "")
    random_string = ''.join(choice(ascii_lowercase + digits) for i in range(6))
    return '{0}_{1}'.format(name, random_string)


def check_dirs_destiny(path, client):
    """First need to know if the dirs schema exist"""
    try:
        exist = True
        sftp = client.open_sftp()
        try:
            sftp.listdir(path)
        except IOError:
            sftp.mkdir(path)
        sftp.close()
    except Exception as error:
        exist = False
    return exist


def search_for_script_names(script):
    _items = dict()
    result = []
    try:
        kwd_names = Keyword.objects.values_list('name', flat=True)
        for name in kwd_names:
            if name in script:
                kwd = Keyword.objects.get(name=name)
                result.append(kwd.id)
            _items['items'] = result
    except Exception as error:
        _items['error'] = error
    return _items


def search_for_libraries_names(script):
    _items = dict()
    result = []
    try:
        _names = Source.objects.filter(category=5, depends__category=4).values_list('name', flat=True)
        for name in _names:
            if name in script:
                library = Source.objects.get(name=name)
                result.append(library.id)
            _items['items'] = result
    except Exception as error:
        _items['error'] = error
    return _items


def send_files(filename, file_type, config, client):
    """sent files Via SSH"""
    _data = dict()
    try:
        path = config.get('path')
        dirs = ['Keywords', 'Libraries', 'Profiles', 'Resources', 'Templates', 'TestScripts', 'Tools', 'TestSuites',
                'Results']
        for directory in dirs:
            new_path = "{0}/{1}".format(path, directory)
            res = check_dirs_destiny(new_path, client)
            if not res:
                raise Exception("Destination directory does not exist, you don't have write permission.")
        """SCPCLient takes a paramiko transport as its only argument"""
        scp = SCPClient(client.get_transport())
        scp.put(filename, remote_path='{0}/{1}'.format(path, dirs[file_type]))
        scp.close()
    except Exception as error:
        _data['text'] = error
    return _data


def run_script(filename, params, client, type_script):
    """This execute pybot with some flags """
    _data = dict()
    try:
        exec_command = "../TestScripts/{0}_test_case.robot".format(filename)
        if type_script is 3:
            exec_command = "../TestSuites/{0}_test_suite.robot".format(filename)
        config = params.get('config')
        arguments = params.get('global_variables')
        if arguments:
            stdin, stdout, stderr = client.exec_command("cd {0}/Results && pybot -V ../Profiles/{1}_profile.py"
                                                        " -o {1}_output.xml"
                                                        " -l {1}_log.html"
                                                        " -r {1}_report.html {2}".format(config.get('path'),
                                                                                         filename,
                                                                                         exec_command),
                                                        get_pty=True)
            stdin.flush()
            output = "{0}".format(stdout.read())
        else:
            stdin, stdout, stderr = client.exec_command("cd {0}/Results && pybot "
                                                        " -o {1}_output.xml"
                                                        " -l {1}_log.html"
                                                        " -r {1}_report.html {2}".format(config.get('path'),
                                                                                         filename,
                                                                                         exec_command),
                                                        get_pty=True)
            stdin.flush()
            output = "{0}".format(stdout.read())
        if "command not found: pybot" in output:
            raise Exception(output)
        else:
            _data['text'] = stdout.read()
    except Exception as error:
        _data['error'] = error
    return _data


def get_libraries(obj=None, extra=None):
    libraries = []
    current = []
    if obj:
        for element in obj:
            _id = element.get('source')
            if _id not in current:
                libraries.append(Source.objects.get(pk=_id).name)
                current.append(_id)
    if extra:
        for element in extra:
            _id = element.get('items')
            if _id not in current:
                libraries.append(Source.objects.get(pk=_id).name)
                current.append(_id)
    return libraries


def generate_profile(params, filename):
    arguments = params.get('global_variables')
    variables = []
    var_file = open("{0}/profiles/{1}_profile.py".format(settings.MEDIA_ROOT, filename), "w")
    var_file.write("#!/usr/bin/env python\n\n")
    for arg in arguments:
        param = Parameters.objects.get(pk=arg.get('id'))
        variables.append("{0} = {1}\n".format(param.name, arg.get('value')))
    for var in variables:
        var_file.write(var)
    var_file.close()
    return var_file.name


def generate_resource_files(extra_import):
    list_resources = []
    pks_useds = []
    try:
        kwds = extra_import.get('keywords')
        extras = extra_import.get('extra_resources')
        if kwds:
            for k in kwds:
                current_pk = k.get('id')
                if current_pk not in pks_useds:
                    result = dict()
                    pks_useds.append(current_pk)
                    obj = Keyword.objects.get(pk=current_pk)
                    filename = generate_filename(obj.name)
                    kwd_file = open("{0}/keywords/{1}_keyword.robot".format(settings.MEDIA_ROOT, filename), "w")
                    kwd_file.write(k.get('script'))
                    kwd_file.close()
                    result['filename'] = filename
                    result['resource'] = kwd_file.name
                    result['name'] = obj.name
                    list_resources.append(result)
        if extras:
            for pk in extras:
                if str(pk) not in pks_useds:
                    result = dict()
                    pks_useds.append(str(pk))
                    obj = Keyword.objects.get(pk=pk)
                    filename = generate_filename(obj.name)
                    kwd_file = open("{0}/keywords/{1}_keyword.robot".format(settings.MEDIA_ROOT, filename), "w")
                    kwd_file.write(obj.script)
                    kwd_file.close()
                    result['filename'] = filename
                    result['resource'] = kwd_file.name
                    result['name'] = obj.name
                    list_resources.append(result)
    except Exception as error:
        list_resources.append(error)
    return list_resources


def generate_file(obj, type_script, params, filename, client):
    _data_result = dict()
    _data = dict()
    try:
        config = params.get('config')
        """Generate robot files"""
        if type_script is 1:
            extra_elements = json.loads(obj.extra_imports)
            libraries = get_libraries(extra_elements.get('extra'))
            extra_libs = search_for_libraries_names(obj.script)
            extra_libraries = get_libraries(extra=extra_libs)
            resources = generate_resource_files(extra_elements)

            """First create the keyword file"""
            kwd_file = open("{0}/test_keywords/{1}_keyword.robot".format(settings.MEDIA_ROOT, filename), "w")
            kwd_file.write(obj.script)
            kwd_file.close()

            """need to know if the dirs schema exist and then send the files"""
            _data = send_files(kwd_file.name, 0, config, client)
            if _data.get('text'):
                raise Exception(_data.get('text'))

            """Then Test Case file"""
            dummy_tc_file = open("{0}/test_keywords/{1}_test_case.robot".format(settings.MEDIA_ROOT, filename), "w")
            dummy_tc_file.write("*** Settings ***\n")
            dummy_tc_file.write("Resource\t{0}/Keywords/{1}_keyword.robot\n".format(config.get('path'), filename))
            """ Adding some resources"""
            if resources:
                for resource in resources:
                    dummy_tc_file.write("Resource\t{0}/Keywords/{1}_keyword.robot\n".format(
                        config.get('path'),
                        resource.get('filename')
                    ))
                    _data = send_files(resource.get('resource'), 0, config, client)
                    if _data.get('text'):
                        raise Exception(_data.get('text'))
            """Now add the libraries """
            if libraries:
                for lib in libraries:
                    dummy_tc_file.write("Library\t\t{0}\n".format(lib))
                dummy_tc_file.write("\n")
            if extra_libraries:
                for lib in extra_libraries:
                    dummy_tc_file.write("Library\t\t{0}\n".format(lib))
                dummy_tc_file.write("\n")
            dummy_tc_file.write("*** Test Cases ***")
            dummy_tc_file.write("\n")
            dummy_tc_file.write('Test {}'.format(obj.name.replace(" ", "")))
            dummy_tc_file.write("\n")
            dummy_tc_file.write("\t")
            dummy_tc_file.write("[Tags]  TestKeyword")
            dummy_tc_file.write("\n")
            dummy_tc_file.write("\t")
            dummy_tc_file.write(obj.name)
            dummy_tc_file.write("\n")
            dummy_tc_file.close()

            send_files(dummy_tc_file.name, 5, config, client)

        elif type_script is 2:
            items = search_for_script_names(obj.script)
            if items.get('error'):
                raise Exception(items.get('error'))

            extra_elements = json.loads(obj.extra_imports)
            extra_elements['extra_resources'] = items.get('items')
            resources = generate_resource_files(extra_elements)
            libraries = get_libraries(extra_elements.get('extra'))
            extra_libs = search_for_libraries_names(obj.script)
            extra_libraries = get_libraries(extra=extra_libs)

            """ Test Case"""
            tc_file = open("{0}/test_cases/{1}_test_case.robot".format(settings.MEDIA_ROOT, filename), "w")
            tc_file.write("*** Settings ***\n")
            """ Adding some resources"""
            if resources:
                for resource in resources:
                    tc_file.write("Resource\t{0}/Keywords/{1}_keyword.robot\n".format(
                        config.get('path'),
                        resource.get('filename')
                    ))
                    _data = send_files(resource.get('resource'), 0, config, client)
                    if _data.get('text'):
                        raise Exception(_data.get('text'))
            """Now add the libraries """
            if libraries:
                for lib in libraries:
                    tc_file.write("Library\t{0}\n".format(lib))
                tc_file.write("\n")
            if extra_libraries:
                for lib in extra_libraries:
                    tc_file.write("Library\t\t{0}\n".format(lib))
            tc_file.write(obj.script)
            tc_file.close()
            send_files(tc_file.name, 5, config, client)

        elif type_script is 3:
            """Test Suite """
            items = search_for_script_names(obj.script)
            if items.get('error'):
                raise Exception(items.get('error'))

            extra_elements = json.loads(obj.extra_imports)
            libraries = get_libraries(extra_elements.get('extra'))
            extra_libs = search_for_libraries_names(obj.script)
            extra_libraries = get_libraries(extra=extra_libs)
            extra_elements['extra_resources'] = items.get('items')
            kwd_resources = generate_resource_files(extra_elements)
            ts_file = open("{0}/test_suites/{1}_test_suite.robot".format(settings.MEDIA_ROOT, filename),
                           "w")
            ts_file.write("*** Settings ***\n")
            if obj.description:
                ts_file.write("Documentation\t{0}".format(obj.description))
                ts_file.write("\n")
            """ Adding some resources"""
            if kwd_resources:
                """First keywords"""
                for kwd in kwd_resources:
                    ts_file.write("Resource\t{0}/Keywords/{1}_keyword.robot\n".format(
                        config.get('path'),
                        kwd.get('filename')
                    ))
                    _data = send_files(kwd.get('resource'), 0, config, client)
                    if _data.get('text'):
                        raise Exception(_data.get('text'))
            """Now add the libraries """
            if libraries:
                for lib in libraries:
                    ts_file.write("Library\t{0}\n".format(lib))
            if extra_libraries:
                for lib in extra_libraries:
                    ts_file.write("Library\t\t{0}\n".format(lib))
            ts_file.write(obj.script)
            ts_file.close()
            check = send_files(ts_file.name, 7, config, client)
            if check.get('text'):
                raise Exception(check.get('text'))

        elif type_script is 4:
            """ Imported Keywords """
            """ Dummy Test Case file"""
            dummy_tc_file = open("{0}/test_keywords/{1}_test_case.robot".format(settings.MEDIA_ROOT, filename),
                                 "w")
            dummy_tc_file.write("*** Settings ***\n")
            libraries = Source.objects.filter(category=5, depends__category=4)
            for lib in libraries:
                dummy_tc_file.write("Library\t\t{0}\n".format(lib.name))
            dummy_tc_file.write("\n")
            dummy_tc_file.write(obj.script)
            dummy_tc_file.close()
            check = send_files(dummy_tc_file.name, 5, config, client)
            if check.get('text'):
                raise Exception(check.get('text'))

        """Need a variables Profile File"""
        arguments = params.get('global_variables')
        if arguments:
            profile = generate_profile(params, filename)
            send_files(profile, 2, config, client)
        _data_result['text'] = 'Created'
    except Exception as error:
        _data_result['error'] = error
    return _data_result


def get_result_files(client, filename, config):
    """Obtain the Results files (html and xml) for show it"""
    _data = dict()
    try:
        scp = SCPClient(client.get_transport())
        scp.get('{0}/Results/{1}_log.html'.format(config.get('path'), filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.get('{0}/Results/{1}_output.xml'.format(config.get('path'), filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.get('{0}/Results/{1}_report.html'.format(config.get('path'), filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.close()
        client.close()
        _data['text'] = 'Success'
    except Exception as error:
        _data['error'] = error
    return _data


@shared_task()
def run_on_server(_data):
    """The main function to send scripts """
    type_script = _data.get('type_script')
    data_result = dict()
    params = dict()
    profile_category = 0
    try:
        profiles = ServerProfile.objects.filter(pk__in=_data.get('profiles'))
        for profile in profiles:
            if profile.category == 1:
                """is global variables"""
                params['global_variables'] = json.loads(profile.config)
            elif profile.category in [2, 3]:
                """is local connection or jenkins"""
                profile_category = profile.category
                params['config'] = get_config_object(json.loads(profile.config))
        configs = params.get('config')
        filename = _data.get('filename')
        client = get_connection(configs)
        if type_script is 1:
            """is keywords"""
            obj = Keyword.objects.get(id=_data.get('obj_id'))
            if obj.script_type is 2:
                type_script = 4
        elif type_script is 2:
            """is Test Case"""
            obj = TestCase.objects.get(id=_data.get('obj_id'))
        elif type_script is 3:
            """is Test Case"""
            obj = TestSuite.objects.get(id=_data.get('obj_id'))
        _data = generate_file(obj, type_script, params, filename, client)
        if _data.get('error'):
            raise Exception(_data['error'])
        if profile_category is 2:
            """Run pybot only if the user choose -> Local Network connection"""
            result = run_script(filename, params, client, type_script)
            if result.get('error'):
                raise Exception(result.get('error'))
            result = get_result_files(client, filename, configs)
            if result.get('error'):
                raise Exception(result.get('error'))
            data_result['link'] = "{0}/{1}test_result/{2}_report.html".format(settings.SITE_DNS,
                                                                              settings.MEDIA_URL,
                                                                              filename)
        else:
            data_result['text'] = 'Success'
    except Exception as error:
        data_result['error'] = '{0}'.format(error)
    return data_result
