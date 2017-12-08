from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from apps.Servers.models import TemplateServer, ServerProfile, Parameters


class ServerTemplatesListJson(LoginRequiredMixin, BaseDatatableView):
    model = TemplateServer
    columns = ['name', 'description', 'pk']
    order_columns = ['name', 'description', 'pk']
    max_display_length = 200

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return qs


class ServerProfilesListJson(LoginRequiredMixin, BaseDatatableView):
    model = ServerProfile
    columns = ['name', 'description', 'pk']
    order_columns = ['name', 'description', 'pk']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class ParametersListJson(LoginRequiredMixin, BaseDatatableView):
    model = Parameters
    columns = ['name', 'category', 'pk']
    order_columns = ['name', 'category', 'pk']
    max_display_length = 200

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(category__icontains=search)
            )
        return qs
