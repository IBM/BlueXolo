from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from apps.Users.models import User, Task


class UsersListJson(LoginRequiredMixin, BaseDatatableView):
    """ django data tables view is a easy way to get a full data tables on django app
    https://bitbucket.org/pigletto/django-datatables-view
    """
    model = User
    columns = ['first_name', 'last_name', 'email', 'last_login', 'pk']
    order_columns = ['first_name', 'last_name', 'email', 'last_login', 'pk']
    max_display_length = 100

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


class TasksListJson(LoginRequiredMixin, BaseDatatableView):
    """ django data tables view is a easy way to get a full data tables on django app
    https://bitbucket.org/pigletto/django-datatables-view
    """
    model = Task
    columns = ['name', 'state', 'created_at', 'updated_at', 'id']
    order_columns = ['name', 'state', 'created_at', 'updated_at', 'id']
    max_display_length = 100

    def get_initial_queryset(self):
        """get only user tasks"""
        if self.request.user.is_superuser:
            return Task.objects.all()
        user_tasks = self.request.user.get_all_tasks()
        tasks_ids = []
        for t in user_tasks:
            tasks_ids.append(t.id)
        return Task.objects.filter(pk__in=tasks_ids)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(state__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'created_at':
            return '{}'.format(row.created_at.strftime("%d/%b/%Y - %H:%M"))
        if column == 'updated_at':
            return '{}'.format(row.updated_at.strftime("%d/%b/%Y - %H:%M"))
        else:
            return super(TasksListJson, self).render_column(row, column)
