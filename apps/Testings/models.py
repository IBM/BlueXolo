from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.Users.models import User
from apps.Products.models import Source
from apps.Servers.models import ServerProfile

SCRIPT_TYPE_CHOICES = (
    (1, _("Native")),
    (2, _("Imported")),
)


class Collection(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    product = models.ForeignKey(Source, related_name="products")
    user = models.ForeignKey(User)

    class Meta:
        db_table = "collections"
        verbose_name = _('collection')
        verbose_name_plural = _('collections')
        ordering = ['name']

    def __str__(self):
        return '{0}'.format(self.name)


class Keyword(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    user = models.ForeignKey(User)
    script = models.TextField(_('script'))
    values = models.TextField(_('values'), blank=True)
    extra_imports = models.TextField(_('extra imports '), blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    collection = models.ManyToManyField(Collection, blank=True)
    script_type = models.PositiveIntegerField(_('script type'), choices=SCRIPT_TYPE_CHOICES, default=1)

    class Meta:
        db_table = "keywords"
        verbose_name = _('keyword')
        verbose_name_plural = _('keywords')

    def __str__(self):
        return '{0}'.format(self.name)


class Phase(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    product = models.ForeignKey(Source)
    user = models.ForeignKey(User)

    class Meta:
        db_table = "phases"
        verbose_name = _('phase')
        verbose_name_plural = _('phases')

    def __str__(self):
        return '{0}'.format(self.name)


class TestCase(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    script = models.TextField(_('script'), blank=True)
    user = models.ForeignKey(User)
    collection = models.ManyToManyField(Collection)
    functions = models.CharField(_('functions'), blank=True, max_length=100)
    phase = models.ForeignKey(Phase)
    values = models.TextField(_('values'), blank=True)
    extra_imports = models.TextField(_('extra imports '), blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('test case')
        verbose_name_plural = _('test cases')
        db_table = 'testcases'

    def __str__(self):
        return '{0}'.format(self.name)


class TestSuite(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    script = models.TextField(_('script'), blank=True)
    user = models.ForeignKey(User)
    collection = models.ManyToManyField(Collection)
    values = models.TextField(_('values'), blank=True)
    extra_imports = models.TextField(_('extra imports '), blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('test suite')
        verbose_name_plural = _('test suites')
        db_table = 'testsuites'

    def __str__(self):
        return '{0}'.format(self.name)
