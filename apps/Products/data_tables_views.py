from unicodedata import category

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from .models import Argument, Command, Source


class ArgumentsListJson(LoginRequiredMixin, BaseDatatableView):
    model = Argument
    columns = ['name', 'description', 'pk']
    order_columns = ['name', 'description', 'pk']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return qs


class OSCommandsListJson(LoginRequiredMixin, BaseDatatableView):
    model = Command
    columns = ['name', 'description', 'source', 'pk']
    order_columns = ['name', 'description', 'source', 'pk']
    max_display_length = 100

    def get_initial_queryset(self):
        category = self.request.GET.get('category')
        if category:
            qs = Command.objects.filter(source__category=category)
        else:
            qs = Command.objects.all()
        return qs

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__iexact=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'source':
            os_list = []
            for os in row.source.all():
                os_list.append("{}".format(os))
            return os_list
        else:
            return super(OSCommandsListJson, self).render_column(row, column)


class SourcesListJson(LoginRequiredMixin, BaseDatatableView):
    model = Source
    columns = ['name', 'version', 'pk']
    order_columns = ['name', 'version', 'pk']
    max_display_length = 100

    def get_initial_queryset(self):
        _category = self.request.GET.get('category')
        if _category:
            qs = Source.objects.filter(category=_category)
        else:
            qs = Source.objects.all()
        return qs

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs
