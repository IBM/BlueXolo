#!/usr/bin/env python
import csv

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CTAFramework.settings")
from django import setup

setup()

from apps.Servers.models import Parameters, TemplateServer
from apps.Users.models import User


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
            print("Parameters added")
    except Exception as error:
        print(error)

# run_base_migration('parameters_connection.csv', 'BaseConnection', 2)

# run_base_migration('parameters_global.csv', 'GlobalVariables', 1)
