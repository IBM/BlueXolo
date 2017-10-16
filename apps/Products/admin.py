from django.contrib import admin

from .models import Command, Argument, Source

admin.site.register(Command)
admin.site.register(Argument)
admin.site.register(Source)
