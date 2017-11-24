#!/usr/bin/env python
import csv

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CTAFramework.settings")
from django import setup

setup()

from apps.Servers.models import Parameters


def run(name):
    base_path = os.path.dirname(__file__)
    file = os.path.join(base_path,  'base_migrations', name)
    try:
        with open(file) as f:
            reader = csv.reader(f, dialect='excel')
            for idx, row in enumerate(reader):
                if not idx == 0:
                    param, created = Parameters.objects.get_or_create(
                        name=row[0],
                        help_text=row[1],
                        category=row[2],
                        value_type=row[3]
                    )
                    print(param)
            print("Parameters added")
    except Exception as error:
        print(error)


run('parameters.csv')
