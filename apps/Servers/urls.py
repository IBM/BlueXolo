from django.conf.urls import url
from .views import ServerTemplateView, NewServerTemplate, EditServerTemplate, DeleteServerTemplate, ServerProfileView, \
    NewServerProfileView, EditServerProfileView, \
    DeleteServerProfile, ParametersView, NewParametersView, EditParametersView, DeleteParametersView

urlpatterns = [
    # Templates CRUD
    url(r'^templates/$', ServerTemplateView.as_view(), name='servers-templates'),
    url(r'^templates/new/$', NewServerTemplate.as_view(), name='new-server-template'),
    url(r'^templates/(?P<pk>\d+)/$', EditServerTemplate.as_view(), name='edit-server-template'),
    url(r'^templates/(?P<pk>\d+)/delete/$', DeleteServerTemplate.as_view(), name='delete-server-template'),
    # Profiles CRUD
    url(r'^profiles/$', ServerProfileView.as_view(), name='servers-profiles'),
    url(r'^profiles/new/$', NewServerProfileView.as_view(), name='new-server-profile'),
    url(r'^profiles/(?P<pk>\d+)/$', EditServerProfileView.as_view(), name='edit-server-profile'),
    url(r'^profiles/(?P<pk>\d+)/delete/$', DeleteServerProfile.as_view(), name='delete-server-profile'),
    # Parameters CRUD
    url(r'^parameters/$', ParametersView.as_view(), name='parameters'),
    url(r'^parameters/new$', NewParametersView.as_view(), name='new-parameters'),
    url(r'^parameters/(?P<pk>\d+)/$', EditParametersView.as_view(), name='edit-parameters'),
    url(r'^parameters/(?P<pk>\d+)/delete/$', DeleteParametersView.as_view(), name='delete-parameters'),
    # Stepper
    url(r'^templates/(?P<stepper>[-\w]+)/new/$', NewServerTemplate.as_view(), name='new-server-template-stepper'),
    url(r'^profiles/(?P<stepper>[-\w]+)/new/$', NewServerProfileView.as_view(), name='new-server-profile-stepper'),
    url(r'^parameters/(?P<stepper>[-\w]+)/new$', NewParametersView.as_view(), name='new-parameters-stepper'),
]
