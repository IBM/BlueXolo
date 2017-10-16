from django.db import models
from django.utils.translation import ugettext_lazy as _


class Source(models.Model):
    CATEGORY_CHOICES = (
        (1, 'Flow Sentences'),
        (2, 'OS'),
        (3, 'Product'),
        (4, 'Robot Framework'),
        (5, 'External Libraries'),
    )
    name = models.CharField(_('source name'), max_length=255)
    version = models.CharField(_('version'), max_length=100)
    category = models.IntegerField(_('category'), choices=CATEGORY_CHOICES)
    depends = models.ManyToManyField('Source', blank=True)

    class Meta:
        verbose_name = _('source')
        verbose_name_plural = _('sources')
        db_table = 'sources'

    def __str__(self):
        """ Return name and version"""
        return "{0} - {1}".format(self.name, self.version)


class Argument(models.Model):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    requirement = models.BooleanField(default=False)
    needs_value = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('argument')
        verbose_name_plural = _('arguments')
        db_table = 'arguments'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.name)


class Command(models.Model):
    name = models.CharField(_('command'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    arguments = models.ManyToManyField(Argument, blank=True)
    source = models.ManyToManyField(Source, blank=True)

    class Meta:
        verbose_name = _('command')
        verbose_name_plural = _('commands')
        db_table = 'commands'
        ordering = ['name']

    def __str__(self):
        """Return the name command"""
        return "{}".format(self.name)
