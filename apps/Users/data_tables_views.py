from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from apps.Users.models import User


class UsersListJson(LoginRequiredMixin, BaseDatatableView):
    """ django data tables view is a easy way to get a full data tables on django app
    https://bitbucket.org/pigletto/django-datatables-view
    """
    model = User
    columns = ['first_name', 'last_name', 'email', 'last_login', 'pk']
    order_columns = ['first_name', 'last_name', 'email', 'last_login', 'pk']
    max_display_length = 200

    def get_initial_queryset(self):
        """Excluding the admins users"""
        return User.objects.exclude(is_superuser=True)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'last_login':
            return '{}'.format(row.last_login.strftime("%d/%b/%Y - %H:%M"))
        else:
            return super(UsersListJson, self).render_column(row, column)
