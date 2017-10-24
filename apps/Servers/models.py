from django.db import models
from django.utils.translation import ugettext_lazy as _

VARIABLES = 1
LOCAL = 2
JENKINS = 3
CATEGORY_CHOICES = (
    (VARIABLES, 'Global Variables'),
    (LOCAL, 'Local Network Connection'),
    (JENKINS, 'Jenkins Connection'),
)


class Parameters(models.Model):
    VALUES_TYPES_CHOICES = (
        (1, 'String'),
        (2, 'List'),
    )
    name = models.CharField(_('name'), max_length=100)
    help_text = models.CharField(_('help text'), max_length=255, blank=True)
    category = models.IntegerField(_('category'), choices=CATEGORY_CHOICES, default=1)
    value_type = models.IntegerField(_('category'), choices=VALUES_TYPES_CHOICES, default=1)

    class Meta:
        db_table = 'parameters'
        verbose_name = _('parameter')
        verbose_name_plural = _('parameters')
        ordering = ['name']

    def __str__(self):
        return '{0}'.format(self.name)


class TemplateServer(models.Model):
    name = models.CharField(_('name'), max_length=30)
    description = models.TextField(_('description'), blank=True)
    category = models.IntegerField(_('category'), choices=CATEGORY_CHOICES, default=1)
    parameters = models.ManyToManyField(Parameters, blank=True)

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
    category = models.IntegerField(_('category'), choices=CATEGORY_CHOICES, default=1)

    class Meta:
        db_table = 'servers_profiles'
        verbose_name = _('server_profile')
        verbose_name_plural = _('server_profiles')

    def __str__(self):
        return '{0}'.format(self.name)
