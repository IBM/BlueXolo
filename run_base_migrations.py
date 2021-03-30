#!/usr/bin/env python
import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CTAFramework.settings")
from django import setup

setup()

from apps.Servers.models import Parameters, TemplateServer
from apps.Users.models import User

def create_superuser():
    try:
        user = User.objects.get(pk=1)
        print("Superuser already created.")
        pass
    except User.DoesNotExist:
        DJANGO_SU_EMAIL = os.environ.get('ADMIN_MAIL')
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD')

        superuser = User.objects.create_superuser(
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD)
        superuser.save()
        print("Superuser created successfully with password {}".format(DJANGO_SU_PASSWORD))


def run_base_migration(file_name, template_name=None, category=None):
    """Function for add parameters from csv file.
    @param file_name[String] = something.csv
    @param template_name[String][Optional] = ExampleTemplate
    @param category[Integer][Optional] = 1 
    """
    base_path = os.path.dirname(__file__)
    file = os.path.join(base_path, 'base_migrations', file_name)
    user = User.objects.get(pk=1)
    try:
        if template_name and category:
            template, created = TemplateServer.objects.get_or_create(
                name=template_name,
                description="Base template from base migration",
                category=category,
                user=user
            )
        if created:
            with open(file) as f:
                reader = csv.reader(f, dialect='excel')
                for idx, row in enumerate(reader):
                    if not idx == 0:
                        param, created = Parameters.objects.get_or_create(
                            name=row[0],
                            help_text=row[1],
                            category=row[2],
                            value_type=row[3],
                            user=user
                        )
                        if template_name and category:
                            template.parameters.add(param)
                        print(param)
                print("{} parameters added.".format(template_name))
        else:
            print("{} parameters already added.".format(template_name))
    except Exception as error:
        print(error)

# Create super user
create_superuser()

# Connection Profile
run_base_migration('parameters_connection.csv', 'BaseConnection', 2)
# Global variables Profile
run_base_migration('parameters_global.csv', 'GlobalVariables', 1)
