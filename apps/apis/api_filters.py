from django_filters import rest_framework as filters

from apps.Products.models import Source, Argument
from apps.Testings.models import Collection
from apps.Users.models import Task


class SourceFilter(filters.FilterSet):
    class Meta:
        model = Source
        fields = ('category', 'id')


class CollectionFilter(filters.FilterSet):
    class Meta:
        model = Collection
        fields = ('name', 'id')


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = ('name', 'id', 'task_id')


class ArgumentFilter(filters.FilterSet):
    class Meta:
        model = Argument
        fields = ('name', 'id')
