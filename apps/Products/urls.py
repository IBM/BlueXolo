from django.conf.urls import url

from .views import HomeView, IndexView, ArgumentsView, NewArgumentView, EditArgumentView, DeleteArgumentView, \
    SourceList, CreateSourceView, DeleteSourceView, EditSourceView, CommandsView, EditCommandView, NewCommandView, \
    DeleteCommandView, PhasesView, NewPhaseView, EditPhaseView, DeletePhaseView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^home/$', HomeView.as_view(), name="home"),
    # Arguments CRUD
    url(r'^arguments/$', ArgumentsView.as_view(), name="arguments"),
    url(r'^arguments/(?P<cmd>\d+)/new$', NewArgumentView.as_view(), name="new-argument"),
    url(r'^arguments/(?P<pk>\d+)/$', EditArgumentView.as_view(), name='edit-argument'),
    url(r'^arguments/(?P<pk>\d+)/delete/$', DeleteArgumentView.as_view(), name='delete-argument'),
    # Sources
    url(r'^sources/(?P<slug>[-\w]+)/$', SourceList.as_view(), name='source-list'),
    url(r'^sources/(?P<slug>[-\w]+)/new/$', CreateSourceView.as_view(), name='new-source'),
    url(r'^sources/(?P<pk>\d+)/edit/$', EditSourceView.as_view(), name='edit-source'),
    url(r'^sources/(?P<pk>\d+)/delete/$', DeleteSourceView.as_view(), name='delete-source'),
    # Commands
    url(r'^commands/$', CommandsView.as_view(), name='commands'),
    url(r'^commands/new/$', NewCommandView.as_view(), name='new-command'),
    url(r'^commands/(?P<pk>\d+)/edit/$', EditCommandView.as_view(), name='edit-command'),
    url(r'^commands/(?P<pk>\d+)/delete/$', DeleteCommandView.as_view(), name='delete-command'),
    # phases
    url(r'^phases/$', PhasesView.as_view(), name='phases'),
    url(r'^phases/new/$', NewPhaseView.as_view(), name='new-phase'),
    url(r'^phases/(?P<pk>\d+)/edit/$', EditPhaseView.as_view(), name='edit-phase'),
    url(r'^phases/(?P<pk>\d+)/delete/$', DeletePhaseView.as_view(), name='delete-phase'),
]
