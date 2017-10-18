from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.Users.models import User
from apps.Products.models import Source


class Keyword(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    user = models.ForeignKey(User)
    script = models.TextField(_('script'))
    values = models.TextField(_('values'), blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        db_table = "keywords"
        verbose_name = _('keyword')
        verbose_name_plural = _('keywords')

    def __str__(self):
        return '{0}'.format(self.name)


class Collection(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    product = models.ForeignKey(Source, related_name="products")
    keywords = models.ManyToManyField(Keyword, blank=True)

    class Meta:
        db_table = "collections"
        verbose_name = _('collection')
        verbose_name_plural = _('collections')
        ordering = ['name']

    def __str__(self):
        return '{0}'.format(self.name)
