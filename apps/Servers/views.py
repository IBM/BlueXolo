import paramiko
import pexpect
import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from pexpect import pxssh
from random import choice
from scp import SCPClient
from string import digits, ascii_lowercase

from .forms import ServerProfileForm, NewJenkinsServerprofileForm
from .models import TemplateServer, ServerProfile

from celery import shared_task


class ServerTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "servers-templates.html"


class NewServerTemplate(LoginRequiredMixin, TemplateView):
    template_name = "create-server-template.html"


class EditServerTemplate(LoginRequiredMixin, DetailView):
    model = TemplateServer
    template_name = "edit-server-template.html"


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


class JenkinsServerProfileView(LoginRequiredMixin, TemplateView):
    template_name = "jenkins-server-profiles.html"


class NewJenkinsServerProfileView(LoginRequiredMixin, CreateView):
    template_name = "create-edit-jenkins-server-profile.html"
    form_class = NewJenkinsServerprofileForm
    success_url = reverse_lazy('jenkins-servers-profiles')

    def get_context_data(self, **kwargs):
        context = super(NewJenkinsServerProfileView, self).get_context_data(**kwargs)
        context['title'] = 'New Jenkins Profile'
        return context


@shared_task
def run_keyword(host, user, passwd, filename, script, values, path):
    ssh = SshConnect()
    ssh.create_robot_file(filename, script)
    ssh.create_testcase_robotFile(filename, values)
    ssh.send_file_user_pass(filename, host, user, passwd, path)
    result, result_filename = ssh.run_file_named(filename, host, user, passwd, path)
    ssh.send_results_named(host, user, passwd, result_filename, path)
    return result, result_filename


class SshConnect(LoginRequiredMixin):
    def send_file_user_pass(self, filename, host, user, passwd, path):
        name = filename.replace(" ", "")
        command_keyword = 'scp {0}/test_keywords/{1}_keyword.robot {2}@{3}:{4}'.format(
            settings.MEDIA_ROOT,
            name,
            user,
            host,
            path
        )
        command_testcase = 'scp {0}/test_keywords/{1}_testcase.robot {2}@{3}:{4}'.format(
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

    def run_file_named(self, filename, host, user, passwd, path):
        name = filename.replace(" ", "")
        ssh = pxssh.pxssh(timeout=50)
        ssh.login(host, user, passwd)
        random_string = ''.join(choice(ascii_lowercase + digits) for i in range(12))
        run_path = 'cd {0}'.format(path)
        today = time.strftime("%y_%m_%d")
        try:
            run_keyword = 'pybot -o {0}_{1}_{2}_output.xml -l {0}_{1}_{2}_log.html -r {0}_{1}_{2}_report.html {0}_testcase.robot'.format(
                name,
                random_string,
                today
            )
            print(run_keyword)
            ssh.sendline(run_path)
            ssh.sendline(run_keyword)
            ssh.prompt()
            ssh_result = ssh.before
            ssh.logout()
            return ssh_result, "{0}_{1}_{2}".format(name, random_string, today)
        except Exception as error:
            return error

    def send_results_named(self, host, user, passwd, filename, path):
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=passwd)
        scp = SCPClient(t)
        scp.get('{0}/{1}_log.html'.format(path, filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.get('{0}/{1}_report.html'.format(path, filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.get('{0}/{1}_output.xml'.format(path, filename),
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
