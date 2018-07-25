from django.db import models
from django.utils.translation import ugettext_lazy as _


class Source(models.Model):
    """
    Source

    Model used to keep the source of command and arguments:

        name - CharField
        version - CharField
        category - IntegerField
        depends - ManyToManyField('Source')

    Category can be:
        1   -   Flow Sentences
        2   -   OS
        3   -   Product
        4   -   Robot Framework
        5   -   External Libraries
    """
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
        """ Returns name and version"""
        return "{0} - {1}".format(self.name, self.version)


class Command(models.Model):
    """
    Command

    Model used to keep the commands of a product or OS:

        name - CharField
        description - TextField
        source - ManyToManyField(Source)
    """
    name = models.CharField(_('command'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    source = models.ManyToManyField(Source, blank=True)

    class Meta:
        verbose_name = _('command')
        verbose_name_plural = _('commands')
        db_table = 'commands'
        ordering = ['name']

    def __str__(self):
        """Returns the command name"""
        return "{}".format(self.name)

    def get_arguments(self):
        """
        get_arguments(self)

        Returns the list of arguments (if exists) related to "self"
        """
        return self.argument_set.all()

    def total_arguments(self):
        """
        total_arguments(self)

        Returns the number of arguments associated to "self"
        """
        return count(self.get_arguments())

    def arguments(self):
        args = []
        for argument in self.get_arguments():
            args.append({
                "id": argument.id,
                "name": argument.name,
                "description": argument.description,
                "requirement": argument.requirement,
                "needs_value": argument.needs_value,
            })
        return args

    # TODO: Remove this in future versions of django
    def delete(self):
        for arg in Argument.objects.filter(command=self):
            arg.delete()
        return super(Command, self).delete()


class Argument(models.Model):
    """
    Argument

    Model used to keep the arguments of commands

        command - ForeignKey(Command)
        name - CharField
        description - TextField
        requirement - BooleanField
        needs_value - BooleanField
        include - ManyToManyField('Argument') - It is used to set all arguments that should be included when this one is included
        exclude - ManyToManyField('Argument') - It is used to set all arguments that should be excluded when this one is included
    """
    command = models.ForeignKey(Command, on_delete=models.CASCADE, null=True)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    requirement = models.BooleanField(default=False)
    needs_value = models.BooleanField(default=False)
    include = models.ManyToManyField('self', verbose_name=_("include"), blank=True, related_name='include', help_text="Choose mandatory parameters if this is set.")
    exclude = models.ManyToManyField('self', verbose_name=_("exclude"), blank=True, related_name='exclude', help_text="Choose parameters that should be excluded if this is set.")

    class Meta:
        verbose_name = _('argument')
        verbose_name_plural = _('arguments')
        db_table = 'arguments'
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.name)
