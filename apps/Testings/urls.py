from django.conf.urls import url

from .views import KeyWordsView, NewKeywordView, DeleteKeywordView, CollectionsView, NewCollectionsView, EditCollectionsView, DeleteCollectionsView

urlpatterns = [
    url(r'^keywords/$', KeyWordsView.as_view(), name="keywords"),
    url(r'^keywords/new/$', NewKeywordView.as_view(), name="new-keywords"),
    url(r'^keywords/(?P<pk>\d+)/delete/$', DeleteKeywordView.as_view(), name="delete-keywords"),
    url(r'^collections/$', CollectionsView.as_view(), name="collections"),
    url(r'^collections/new/$', NewCollectionsView.as_view(), name="new-collections"),
    url(r'^collections/(?P<pk>\d+)/$', EditCollectionsView.as_view() , name='edit-collections'),
    url(r'^collections/(?P<pk>\d+)/delete/$', DeleteCollectionsView.as_view(), name="delete-collections"),
]
