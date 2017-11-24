import django_filters

from apps.Products.models import Source, Argument
from apps.Servers.models import Parameters
from apps.Testings.models import Collection, TestCase, Keyword, Phase, TestSuite
from apps.Users.models import Task


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = ('category', 'id')


class CollectionFilter(django_filters.FilterSet):
    class Meta:
        model = Collection
        fields = ('name', 'id')


class KeywordFilter(django_filters.FilterSet):
    class Meta:
        model = Keyword
        fields = ('collection', 'id', 'name')


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ('name', 'id', 'task_id')


class ArgumentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Argument
        fields = ('name', 'id')


class ParametersFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Parameters
        fields = ('name', 'id', 'category')


class TestCaseFilter(django_filters.FilterSet):
    class Meta:
        model = TestCase
        fields = ('name', 'id', 'collection')


class PhaseFilter(django_filters.FilterSet):
    class Meta:
        model = Phase
        fields = ('name', 'id')


class TestSuiteFilter(django_filters.FilterSet):
    class Meta:
        model = TestSuite
        fields = ('name', 'id')
