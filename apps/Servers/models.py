from django.db import models
from django.utils.translation import ugettext_lazy as _


class TemplateServer(models.Model):
    name = models.CharField(_('name'), max_length=30)
    description = models.TextField(_('description'), blank=True)
    parameters = models.TextField(_('parameters'))

    class Meta:
        db_table = 'servers_templates'
        verbose_name = _('server_template')
        verbose_name_plural = _('servers_templates')

    def __str__(self):
        return "{}".format(self.name)


class ServerProfile(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=30)
    description = models.TextField(_('description'), blank=True)
    template = models.ForeignKey(TemplateServer)
    config = models.TextField(blank=True)

    class Meta:
        db_table = 'servers_profiles'
        verbose_name = _('server_profile')
        verbose_name_plural = _('server_profiles')

    def __str__(self):
        return '{0}'.format(self.name)


class JenkinsServerProfile(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=30)
    ip = models.CharField(_('ip'), unique=True, max_length=15)
    port = models.CharField(_('port'), max_length=5)

    class Meta:
        db_table = 'jenkins_servers_profiles'
        verbose_name = _('jenkins_server_profile')
        verbose_name_plural = _('jenkins_server_profiles')

    def __str__(self):
        return '{0}:{1}'.format(self.ip, self.ip)
