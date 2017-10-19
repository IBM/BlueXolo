from django.conf.urls import url

from apps.Products.data_tables_views import ArgumentsListJson, OSCommandsListJson, SourcesListJson
from apps.Servers.data_tables_views import ServerTemplatesListJson, ServerProfilesListJson, \
    JenkinsServerProfilesListJson
from apps.Testings.data_tables_views import KeywordsListJson, CollectionsListJson
from .views import KeywordAPIView, ServerTemplateApiView, \
    ServerTemplateDetailApiView, ServerProfileApiView, ServerProfileDetailApiView, KeywordDetailApiView, \
    CommandsApiView, CommandsDetailApiView, RunExtract, SourceApiView, CollectionApiView, RunOnServerApiView, \
    TasksApiView, ArgumentsApiView

urlpatterns = [
    url(r'^arguments/$', ArgumentsApiView.as_view(), name="api-arguments"),
    url(r'^commands/$', CommandsApiView.as_view(), name="api-commands"),
    url(r'^commands/(?P<pk>[0-9]+)/$', CommandsDetailApiView.as_view(), name="api-commands"),
    url(r'^templates/$', ServerTemplateApiView.as_view(), name="api-templates"),
    url(r'^templates/(?P<pk>[0-9]+)/$', ServerTemplateDetailApiView.as_view(), name="api-templates"),
    url(r'^profiles/$', ServerProfileApiView.as_view(), name="api-profiles"),
    url(r'^profiles/(?P<pk>[0-9]+)/$', ServerProfileDetailApiView.as_view(), name="api-profiles"),
    url(r'^keywords/$', KeywordAPIView.as_view(), name="api-keywords"),
    url(r'^keywords/(?P<pk>[0-9]+)/$', KeywordDetailApiView.as_view(), name="api-keywords"),
    url(r'^source/$', SourceApiView.as_view(), name="api-source"),
    url(r'^collection/$', CollectionApiView.as_view(), name="api-collection"),
    url(r'^tasks/$', TasksApiView.as_view(), name="api-tasks"),
    # DataTables Api
    url(r'^commands/arguments/$', ArgumentsListJson.as_view(), name="api-commands-arguments"),
    url(r'^commands/os/$', OSCommandsListJson.as_view(), name="api-os-commands"),
    url(r'^servers/templates/$', ServerTemplatesListJson.as_view(), name='api-servers-templates'),
    url(r'^servers/profiles/$', ServerProfilesListJson.as_view(), name='api-servers-profiles'),
    url(r'^servers/jenkins-servers/$', JenkinsServerProfilesListJson.as_view(), name="api-jenkins-servers"),
    url(r'^keywords/list/$', KeywordsListJson.as_view(), name="api-keywords-list"),
    url(r'^collections/$', CollectionsListJson.as_view(), name="api-collections"),
    url(r'^sources/list/$', SourcesListJson.as_view(), name="api-sources-list"),
    # Extract
    url(r'^run_extract/$', RunExtract.as_view(), name="run_extract"),
    # Run On server
    url(r'^run_on_server/$', RunOnServerApiView.as_view(), name="run-on-server"),
]
