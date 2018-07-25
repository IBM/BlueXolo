from django.core.management.base import BaseCommand
from apps.Products import models

class Command(BaseCommand):
    args = '--path <path>'
    help = """initialize_robot
        Usage:
        python manage.py (or ./manage.py) initialize_robot

        Will create the commands / arguments used to handle flow sentences in robot framework
    """


    def handle(self, *args, **kwargs):
        Source = models.Source
        Command = models.Command
        Argument = models.Argument

        source, created = Source.objects.get_or_create(
            name="CTA Framework",
            version="2.0",
            category=1
        )

        # FOR
        for_command, created = Command.objects.get_or_create(
            name="for in"
        )

        start, created = Argument.objects.get_or_create(command=for_command, name="start", description="N/A", needs_value=True, requirement=True)
        end, created = Argument.objects.get_or_create(command=for_command, name="end", description="N/A", needs_value=True, requirement=True)
        start.save()
        end.save()
        for_command.source.add(source)
        for_command.save()

        # FOR in range
        for_in_command, created = Command.objects.get_or_create(
            name="for in range"
        )

        start, created = Argument.objects.get_or_create(command=for_in_command, name="start", description="N/A", needs_value=True, requirement=True)
        end, created = Argument.objects.get_or_create(command=for_in_command, name="end", description="N/A", needs_value=True, requirement=True)
        start.save()
        end.save()
        for_in_command.source.add(source)
        for_in_command.save()

        # Comment
        comment_command, created = Command.objects.get_or_create(
            name="comment"
        )
        comment, created = Argument.objects.get_or_create(command=comment_command, name="comment", description="N/A", needs_value=True,
                                                          requirement=True)
        comment.save()
        comment_command.source.add(source)
        comment_command.save()

        # Variable
        variable_command, created = Command.objects.get_or_create(
            name="variable"
        )
        name, created = Argument.objects.get_or_create(command=variable_command, name="name", description="N/A", needs_value=True, requirement=True)
        value, created = Argument.objects.get_or_create(command=variable_command, name="value", description="N/A", needs_value=True, requirement=True)
        name.save()
        value.save()
        variable_command.source.add(source)
        variable_command.save()

        # Global Variable
        g_variable_command, created = Command.objects.get_or_create(
            name="Global Variable"
        )
        name_g, created = Argument.objects.get_or_create(command=g_variable_command, name="name", description="N/A", needs_value=True, requirement=True)
        value_g, created = Argument.objects.get_or_create(command=g_variable_command, name="value", description="N/A", needs_value=True,
                                                          requirement=True)
        name_g.save()
        value_g.save()
        g_variable_command.source.add(source)
        g_variable_command.save()

        # List
        list_command, created = Command.objects.get_or_create(
            name="List"
        )
        name, created = Argument.objects.get_or_create(command=list_command, name="name", description="N/A", needs_value=True, requirement=True)
        value, created = Argument.objects.get_or_create(command=list_command, name="value", description="N/A", needs_value=True, requirement=True)
        name.save()
        value.save()
        list_command.source.add(source)
        list_command.save()

        # command
        command_command, created = Command.objects.get_or_create(
            name="command"
        )
        command_name, created = Argument.objects.get_or_create(command=command_command, name="name", description="N/A", needs_value=True,
                                                               requirement=True)
        command_name.save()
        command_command.source.add(source)
        command_command.save()

        # Tags
        tags_command, created = Command.objects.get_or_create(
            name="tags"
        )

        tags, created = Argument.objects.get_or_create(command=tags_command, name="tags", description="N/A", needs_value=True, requirement=True)
        name, created = Argument.objects.get_or_create(command=tags_command, name="name", description="N/A", needs_value=True, requirement=True)
        tags_command.source.add(source)
        tags_command.save()
        print('\n  --------------------------------------- Control Flow Sentences Created :3 --------------------------')

