from django.conf.urls import url
from .views import UsersView, CreateUserView, EditUserView, DeleteUserView
from .data_tables_views import UsersListJson

urlpatterns = [
    url(r'^$', UsersView.as_view(), name='users'),
    url(r'^new/$', CreateUserView.as_view(), name='create-user'),
    url(r'^(?P<pk>\d+)/delete/$', DeleteUserView.as_view(), name='delete-user'),
    url(r'^(?P<pk>\d+)$', EditUserView.as_view(), name='edit-user'),
    url(r'^api/users/$', UsersListJson.as_view(), name='api-users'),
]
