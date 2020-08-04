from django.conf.urls import url

from apps.Products.data_tables_views import ArgumentsListJson, OSCommandsListJson, SourcesListJson
from apps.Servers.data_tables_views import ServerTemplatesListJson, ServerProfilesListJson, ParametersListJson
from apps.Testings.data_tables_views import KeywordsListJson, CollectionsListJson, TestcasesListJson, PhasesListJson, \
    TestsuitesListJson, ImportedListJson
from apps.Users.data_tables_views import TasksListJson
from .views import KeywordAPIView, ServerTemplateApiView, \
    ServerTemplateDetailApiView, ServerProfileApiView, ServerProfileDetailApiView, KeywordDetailApiView, \
    CommandsApiView, CommandsDetailApiView, RunExtract, SourceApiView, CollectionApiView, RunOnServerApiView, \
    TasksApiView, ArgumentsApiView, ParametersApiView, TestCaseApiView, TestCaseDetailApiView, ParametersDetailApiView, \
    ArgumentsDetailApiView, PhaseApiView, PhaseDetailApiView, TestSuiteApiView, TestSuiteDetailApiView, \
    get_highlight_version, SearchScriptsAPIView

urlpatterns = [
    url(r'^arguments/$', ArgumentsApiView.as_view(), name="api-arguments"),
    url(r'^arguments/(?P<pk>[0-9]+)/$', ArgumentsDetailApiView.as_view(), name="api-arguments"),
    url(r'^parameters/$', ParametersApiView.as_view(), name="api-parameters"),
    url(r'^parameters/(?P<pk>[0-9]+)/$', ParametersDetailApiView.as_view(), name="api-parameters"),
    url(r'^commands/$', CommandsApiView.as_view(), name="api-commands"),
    url(r'^commands/(?P<pk>[0-9]+)/$', CommandsDetailApiView.as_view(), name="api-commands"),
    url(r'^templates/$', ServerTemplateApiView.as_view(), name="api-templates"),
    url(r'^templates/(?P<pk>[0-9]+)/$', ServerTemplateDetailApiView.as_view(), name="api-templates"),
    url(r'^profiles/$', ServerProfileApiView.as_view(), name="api-profiles"),
    url(r'^profiles/(?P<pk>[0-9]+)/$', ServerProfileDetailApiView.as_view(), name="api-profiles"),
    url(r'^keywords/$', KeywordAPIView.as_view(), name="api-keywords"),
    url(r'^keywords/(?P<pk>[0-9]+)/$', KeywordDetailApiView.as_view(), name="api-keywords"),
    url(r'^testcases/$', TestCaseApiView.as_view(), name="api-testcases"),
    url(r'^testcases/(?P<pk>[0-9]+)/$', TestCaseDetailApiView.as_view(), name="api-testcases"),
    url(r'^phases/$', PhaseApiView.as_view(), name="api-phases"),
    url(r'^phases/(?P<pk>[0-9]+)/$', PhaseDetailApiView.as_view(), name="api-phases"),
    url(r'^testsuite/$', TestSuiteApiView.as_view(), name="api-testsuite"),
    url(r'^testsuite/(?P<pk>[0-9]+)/$', TestSuiteDetailApiView.as_view(), name="api-testsuite"),
    url(r'^source/$', SourceApiView.as_view(), name="api-source"),
    url(r'^collection/$', CollectionApiView.as_view(), name="api-collection"),
    url(r'^tasks/$', TasksApiView.as_view(), name="api-tasks"),
    url(r'^search-script/$', SearchScriptsAPIView.as_view(), name="api-search-script"),
    # DataTables Api
    url(r'^commands/arguments/$', ArgumentsListJson.as_view(), name="api-commands-arguments"),
    url(r'^commands/os/$', OSCommandsListJson.as_view(), name="api-os-commands"),
    url(r'^servers/templates/$', ServerTemplatesListJson.as_view(), name='api-servers-templates'),
    url(r'^servers/profiles/$', ServerProfilesListJson.as_view(), name='api-servers-profiles'),
    url(r'^keywords/list/$', KeywordsListJson.as_view(), name="api-keywords-list"),
    url(r'^testcases/list/$', TestcasesListJson.as_view(), name="api-testcases-list"),
    url(r'^testsuites/list/$', TestsuitesListJson.as_view(), name="api-testsuites-list"),
    url(r'^collections/$', CollectionsListJson.as_view(), name="api-collections"),
    url(r'^sources/list/$', SourcesListJson.as_view(), name="api-sources-list"),
    url(r'^phases/list/$', PhasesListJson.as_view(), name="api-phases-list"),
    url(r'^parameters/list/$', ParametersListJson.as_view(), name="api-parameters-list"),
    url(r'^tasks/list/$', TasksListJson.as_view(), name="api-tasks-list"),
    url(r'^imported/list/(?P<type_script>[\w-]+)/$', ImportedListJson.as_view(), name="api-imported-list"),
    # Extract
    url(r'^run_extract/$', RunExtract.as_view(), name="run_extract"),
    # apply pygment
    url(r'^get-highlight/$', get_highlight_version, name="get-highlight"),
    # Run On server
    url(r'^run_on_server/$', RunOnServerApiView.as_view(), name="run-on-server"),
]
