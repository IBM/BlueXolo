from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from .models import Keyword, Collection


class KeywordsListJson(LoginRequiredMixin, BaseDatatableView):
    model = Keyword
    columns = ['name', 'description', 'created_at', 'pk']
    order_columns = ['name', 'description', 'created_at', 'pk']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'created_at':
            return '{}'.format(row.created_at.strftime("%d/%b/%Y - %H:%M"))
        else:
            return super(KeywordsListJson, self).render_column(row, column)

class CollectionsListJson(LoginRequiredMixin, BaseDatatableView):
    model = Collection
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

