from django.conf.urls import url
from .views import ServerTemplateView, NewServerTemplate, EditServerTemplate, DeleteServerTemplate, ServerProfileView, \
    NewServerProfileView, JenkinsServerProfileView, NewJenkinsServerProfileView, EditServerProfileView, \
    DeleteServerProfile

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
    # Jenkins Servers Profiles
    url(r'^jenkins-profiles/$', JenkinsServerProfileView.as_view(), name='jenkins-servers-profiles'),
    url(r'^jenkins-profiles/new/$', NewJenkinsServerProfileView.as_view(), name='new-jenkins-server-profile'),
]
