import paramiko
import pexpect

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.migrations import serializer
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from pexpect import pxssh
from scp import SCPClient

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


@shared_task
def run_keyword(host, user, passwd, filename, script, values, path, namefile, profilename, variables):
    ssh = SshConnect()
    ssh.create_robot_file(filename, script)
    ssh.create_testcase_robotFile(filename, values)
    ssh.create_profile_file(profilename, variables)
    if not ssh.check_dirs(host, user, passwd, path):
        ssh.create_structure(host, user, passwd, path)
    ssh.send_file_user_pass(filename, host, user, passwd, path)
    ssh.run_file_named(filename, host, user, passwd, path, namefile)
    ssh.send_results_named(host, user, passwd, namefile, path)

@shared_task
def run_keyword_profile(host, user, passwd, filename, script, name_values, path, namefile, profilename, variables):
    ssh = SshConnect()
    ssh.create_robot_file(filename, script)
    ssh.create_testcase_robotFile(filename, name_values)
    ssh.create_profile_file(profilename, variables)
    if not ssh.check_dirs(host, user, passwd, path):
        ssh.create_structure(host, user, passwd, path)
    ssh.send_file_user_pass(filename, host, user, passwd, path)
    ssh.send_profile_file(host, user, passwd, path, profilename)
    ssh.run_file_named_profile(filename, host, user, passwd, path, namefile, profilename)
    ssh.send_results_named(host, user, passwd, namefile, path)

@shared_task
def run_testcases(host, user, passwd, filename, script, path, collection_name, keywords, profilename, variables):
    ssh = SshConnect()
    ssh.create_testcase(filename, script,path, collection_name)
    ssh.create_collection_files(collection_name, keywords)
    ssh.create_profile_file(profilename, variables)
    ssh.send_testcase(host, user, passwd, path, filename)
    ssh.send_keywords_collection(host, user, passwd, path, keywords, collection_name)
    ssh.send_profile_file(host,user, passwd,path, profilename)


class SshConnect(LoginRequiredMixin):

    def check_dirs(self, host, user, passwd, path):
        """Check if dirs schema exist"""
        result = False
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(host, username=user, password=passwd)
        _, stdout, _ = client.exec_command(
            "if test -d '{0}/Keywords'; then echo '1'; else  echo '0'; fi".format(path))
        pre_res = stdout.read()
        res = pre_res.decode('ascii').replace("\n", "")
        if int(res):
            result = True
        return result

    def create_structure(self, host, user, passwd, path):
        ssh = pxssh.pxssh(timeout=50)
        ssh.login(host, user, passwd)
        run_create_path = 'mkdir {0}'.format(path)
        run_path = 'cd {0}'.format(path)
        run_create_structure = 'mkdir Keywords Libraries Profiles Resources Templates TestScripts Tools TestSuites'
        try:
            ssh.sendline(run_create_path)
            ssh.sendline(run_path)
            ssh.sendline(run_create_structure)
            ssh.prompt()
            ssh.logout()
        except Exception as error:
            return error

    def send_file_user_pass(self, filename, host, user, passwd, path):
        name = filename.replace(" ", "")
        command_keyword = 'scp {0}/test_keywords/{1}_keyword.robot {2}@{3}:{4}/Keywords'.format(
            settings.MEDIA_ROOT,
            name,
            user,
            host,
            path
        )
        command_testcase = 'scp {0}/test_keywords/{1}_testcase.robot {2}@{3}:{4}/Keywords'.format(
            settings.MEDIA_ROOT,
            name,
            user,
            host,
            path
        )
        system = pexpect.spawn(command_keyword)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)
        system = pexpect.spawn(command_testcase)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)

    def send_file_profile_user_pass(self, filename, host, user, passwd, path, profilename):
        name = filename.replace(" ", "")
        name_profile = profilename.replace(" ","")
        command_keyword = 'scp {0}/test_keywords/{1}_keyword.robot {2}@{3}:{4}/Keywords'.format(
            settings.MEDIA_ROOT,
            name,
            user,
            host,
            path
        )
        command_testcase = 'scp {0}/test_keywords/{1}_testcase.robot {2}@{3}:{4}/Keywords'.format(
            settings.MEDIA_ROOT,
            name,
            user,
            host,
            path
        )
        system = pexpect.spawn(command_keyword)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)
        system = pexpect.spawn(command_testcase)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)


    def run_file_named(self, filename, host, user, passwd, path, namefile):
        name = filename.replace(" ", "")
        ssh = pxssh.pxssh(timeout=50)
        ssh.login(host, user, passwd)
        run_path = 'cd {0}/Keywords'.format(path)
        try:
            run_keyword = 'pybot -o {0}_output.xml -l {0}_log.html -r {0}_report.html {1}_testcase.robot'.format(
                namefile,
                name
            )
            print(run_keyword)
            ssh.sendline(run_path)
            ssh.sendline(run_keyword)
            ssh.prompt()
            ssh.logout()
        except Exception as error:
            return error

    def run_file_named_profile(self, filename, host, user, passwd, path, namefile, profilename):
        name = filename.replace(" ", "")
        name_profile = profilename.replace(" ","")
        ssh = pxssh.pxssh(timeout=50)
        ssh.login(host, user, passwd)
        run_path = 'cd {0}/Keywords'.format(path)
        try:
            run_keyword = 'pybot -o {0}_output.xml -l {0}_log.html -r {0}_report.html -V {1}/Profiles/{2}.py {3}_testcase.robot'.format(
                namefile,
                path,
                name_profile,
                name
            )
            print(run_keyword)
            ssh.sendline(run_path)
            ssh.sendline(run_keyword)
            ssh.prompt()
            ssh.logout()
        except Exception as error:
            return error

    def send_results_named(self, host, user, passwd, filename, path):
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=passwd)
        scp = SCPClient(t)
        scp.get('{0}/Keywords/{1}_log.html'.format(path, filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.get('{0}/Keywords/{1}_report.html'.format(path, filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.get('{0}/Keywords/{1}_output.xml'.format(path, filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.close()
        t.close()

    def create_robot_file(self, filename, script):
        name = filename.replace(" ", "")
        f = open("{0}/test_keywords/{1}_keyword.robot".format(settings.MEDIA_ROOT, name), "w")
        f.write("*** Keywords ***\n\n")
        f.write(filename)
        f.write("\n")
        f.write("\t")
        f.write(script)
        f.close()

    def create_testcase_robotFile(self, filename, values):
        name = filename.replace(" ", "")
        a = open("{0}/test_keywords/{1}_testcase.robot".format(settings.MEDIA_ROOT, name), "w")
        a.write("*** Settings ***\n\n")
        a.write("Resource\t{}_keyword.robot\n".format(name))
        a.write("Library\tSSHLibrary\n")
        a.write("*** Test Cases ***\n\n")
        name = 'TestCaseTo{}'.format(filename.replace(" ", ""))
        a.write(name)
        a.write("\n")
        a.write("\t")
        a.write(filename)
        a.write("\t")
        for i in range(0, len(values)):
            f = '{}\t'.format(values[i])
            a.write(f)
        a.close()

    def create_keywords_collections(self, filename, script):
        name = filename.replace(" ", "")
        f = open("{0}/keywords/{1}_keyword.robot".format(settings.MEDIA_ROOT, name), "w")
        f.write("*** Keywords ***\n\n")
        f.write(filename)
        f.write("\n")
        f.write("\t")
        f.write(script)
        f.close()

    def create_testcase_robotFile(self, filename, values):
        name = filename.replace(" ", "")
        a = open("{0}/test_keywords/{1}_testcase.robot".format(settings.MEDIA_ROOT, name), "w")
        a.write("*** Settings ***\n\n")
        a.write("Resource\t{}_keyword.robot\n".format(name))
        a.write("Library\tSSHLibrary\n")
        a.write("*** Test Cases ***\n\n")
        name = 'TestCaseTo{}'.format(filename.replace(" ", ""))
        a.write(name)
        a.write("\n")
        a.write("\t")
        a.write(filename)
        a.write("\t")
        for i in range(0, len(values)):
            f = '{}\t'.format(values[i])
            a.write(f)
        a.close()

    def create_collection_files(self, collection_name, keywords):
        name = collection_name.replace(" ","")
        for keyword in keywords:
            self.create_keywords_collections(keyword.name, keyword.script)
        f = open("{0}/keywords/Collection_{1}.robot".format(settings.MEDIA_ROOT, name), "w")
        f.write("*** Collection {0} ***".format(name))
        f.write("\n")
        f.write("*** Settings ***")
        f.write("\n")
        for keyword in keywords:
            _key_name = keyword.name
            f.write("Resource {0}_keyword.robot\n".format(_key_name.replace(" ","")))
        f.close()

    def create_testcase(self, filename, script, path, collection_name):
        name = filename.replace(" ","")
        a = open("{0}/testcases/{1}_testcase.robot".format(settings.MEDIA_ROOT, name), "w")
        a.write("*** Settings ***\n")
        a.write("Resource\t {0}/Keywords/Collection_{1}.robot".format(path, collection_name))
        a.write("\n")
        a.write("*** Test Cases ***")
        a.write("\n")
        a.write("\t{0}".format(script))

    def send_testcase(self,  host, user, passwd,path, filename):
        name = filename.replace(" ", "")
        command_testcase = 'scp {0}/testcases/{1}_testcase.robot {2}@{3}:{4}/Testcases'.format(
            settings.MEDIA_ROOT,
            name,
            user,
            host,
            path
        )
        system = pexpect.spawn(command_testcase)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)

    def send_keywords_collection(self, host, user, passwd,path, keywords, collection_name):
        for keyword in keywords:
            name = keyword.name.replace(" ","")
            command_keyword = 'scp {0}/Keywords/{1}_keyword.robot {2}@{3}:{4}/Keywords'.format(
                settings.MEDIA_ROOT,
                name,
                user,
                host,
                path
            )
            system = pexpect.spawn(command_keyword)
            system.expect('password:')
            system.sendline(passwd)
            system.expect('100%', timeout=600)

        name_collection = collection_name.name.replace(" ", "")
        command_keyword = '{0}/keywords/Collection_{1}.robot {2}@{3}:{4}/Keywords'.format(
            settings.MEDIA_ROOT,
            name_collection,
            user,
            host,
            path
        )
        system = pexpect.spawn(command_keyword)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)

    def create_profile_file(self, profilename, variables):
        name = profilename.replace(" ", "")
        a = open("{0}/profiles/{1}_profile.py".format(settings.MEDIA_ROOT, name), "w")
        a.write("#      {0}      #\n".format(name))
        for p in variables:
            a.write('{0} = "{1}"\n'.format(p[0], p[1]))
        a.close()

    def send_profile_file(self, host, user, passwd, path, profilename):
        name_profile = profilename.replace(" ","")
        command_profile = 'scp {0}/profiles/{1}.py {2}/@{3}:{4}/Profiles'.format(
            settings.MEDIA_ROOT,
            name_profile,
            user,
            host,
            path
        )

        system = pexpect.spawn(command_profile)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)


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
