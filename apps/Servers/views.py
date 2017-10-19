import paramiko
import pexpect
import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from pexpect import pxssh
from scp import SCPClient

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
def run_keyword(host, user, passwd, filename, script, values):
    ssh = SshConnect()
    ssh.create_robot_file(filename, script)
    ssh.create_testcase_robotFile(filename, values)
    ssh.send_file_user_pass(filename, host, user, passwd)
    result = ssh.run_file_named(filename, host, user, passwd)
    ssh.send_results_named(host, user, passwd, filename)
    return result


class SshConnect(LoginRequiredMixin):
    def send_file_user_pass(self, filename, host, user, passwd):
        name = filename.replace(" ", "")
        command_keyword = 'scp {0}/test_keywords/{1}_keyword.robot {2}@{3}:/home/Pruebas/PruebaKeyword'.format(
            settings.MEDIA_ROOT,
            name,
            user,
            host,
        )
        command_testcase = 'scp {0}/test_keywords/{1}_testcase.robot {2}@{3}:/home/Pruebas/PruebaKeyword'.format(
            settings.MEDIA_ROOT,
            name,
            user,
            host,
        )
        system = pexpect.spawn(command_keyword)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)
        system = pexpect.spawn(command_testcase)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)

    def run_file_named(self, filename, host, user, passwd):
        name = filename.replace(" ", "")
        ssh = pxssh.pxssh(timeout=50)
        ssh.login(host, user, passwd)
        dia = time.strftime("%y_%m_%d")
        hora = time.strftime("%H:%M:%S")
        run_path = 'cd /home/Pruebas/PruebaKeyword'
        run_keyword = 'pybot -o {0}_{1}_{2}_output.xml -l {0}_{1}_{2}_log.html -r {0}_{1}_{2}_report.html {3}_testcase.robot'.format(
            dia,
            hora,
            name,
            name,
        )
        ssh.sendline(run_path)
        ssh.sendline(run_keyword)
        ssh.prompt()
        result = ssh.before
        ssh.logout()
        namefile = dia + "_" + hora + "_" + name
        return namefile

    def send_results_named(self, host, user, passwd, filename):
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=passwd)
        scp = SCPClient(t)
        scp.get('/home/Pruebas/PruebaKeyword/{0}_log.html'.format(filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.get('/home/Pruebas/PruebaKeyword/{0}_report.html'.format(filename),
                '{0}/test_result/'.format(settings.MEDIA_ROOT))
        scp.get('/home/Pruebas/PruebaKeyword/{0}_output.xml'.format(filename),
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
