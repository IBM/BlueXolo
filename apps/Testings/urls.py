from django.conf.urls import url

from .views import KeyWordsView, NewKeywordView, DeleteKeywordView, CollectionsView, NewCollectionsView, \
    EditCollectionsView, DeleteCollectionsView, EditKeywordView, TestCaseView, NewTestCaseView, EditTestCaseView, \
    DeleteTestCaseView, TestSuiteView, NewTestSuiteView, EditTestSuiteView, DeleteTestSuiteView, \
    NewKeywordImportedView, EditKeywordImportedView, KeywordsImportedView, DeleteImportedScriptView, RunScriptView

urlpatterns = [
    url(r'^keywords/$', KeyWordsView.as_view(), name="keywords"),
    url(r'^keywords/new/$', NewKeywordView.as_view(), name="new-keywords"),
    url(r'^keywords/edit/(?P<pk>\d+)$', EditKeywordView.as_view(), name="edit-keywords"),
    url(r'^keywords/(?P<pk>\d+)/delete/$', DeleteKeywordView.as_view(), name="delete-keywords"),
    # TestCase
    url(r'^testcases/$', TestCaseView.as_view(), name="testcases"),
    url(r'^testcases/new/$', NewTestCaseView.as_view(), name="new-testcase"),
    url(r'^testcases/edit/(?P<pk>\d+)$', EditTestCaseView.as_view(), name="edit-testcase"),
    url(r'^testcases/(?P<pk>\d+)/delete/$', DeleteTestCaseView.as_view(), name="delete-keywords"),
    # TestSuites
    url(r'^testsuites/$', TestSuiteView.as_view(), name="testsuites"),
    url(r'^testsuites/new/$', NewTestSuiteView.as_view(), name="new-testsuites"),
    url(r'^testsuites/edit/(?P<pk>\d+)$', EditTestSuiteView.as_view(), name="edit-testsuites"),
    url(r'^testsuites/(?P<pk>\d+)/delete/$', DeleteTestSuiteView.as_view(), name="delete-testsuite"),
    # Collections
    url(r'^collections/$', CollectionsView.as_view(), name="collections"),
    url(r'^collections/new/$', NewCollectionsView.as_view(), name="new-collections"),
    url(r'^collections/(?P<pk>\d+)/$', EditCollectionsView.as_view(), name='edit-collections'),
    url(r'^collections/(?P<pk>\d+)/delete/$', DeleteCollectionsView.as_view(), name="delete-collections"),
    # Import
    url(r'^imported/$', KeywordsImportedView.as_view(), name="imported-scripts"),
    url(r'^import/$', NewKeywordImportedView.as_view(), name="new-import-script"),
    url(r'^import/(?P<pk>\d+)/edit/$', EditKeywordImportedView.as_view(), name="edit-import-script"),
    url(r'^import/(?P<pk>\d+)/delete/$', DeleteImportedScriptView.as_view(), name="delete-import-script"),
    # Run scripts
    url(r'^(?P<pk>\d+)/(?P<type_script>\d+)/run$', RunScriptView.as_view(), name="run-script"),
    # Stepper
    url(r'^collections/(?P<stepper>[-\w]+)/new/$', NewCollectionsView.as_view(), name="new-collections-stepper"),
    url(r'^collections/(?P<pk>\d+)/(?P<stepper>[-\w]+)/edit/$', EditCollectionsView.as_view(), name='edit-collections'),
    url(r'^keywords/(?P<stepper>[-\w]+)/new/$', NewKeywordView.as_view(), name="new-keywords-stepper"),
    url(r'^keywords/(?P<pk>\d+)/(?P<stepper>[-\w]+)/edit/$', EditKeywordView.as_view(), name="edit-keywords-stepper"),
    url(r'^testcases/(?P<stepper>[-\w]+)/new/$', NewTestCaseView.as_view(), name="new-testcase-stepper"),
    url(r'^testcases/(?P<pk>\d+)/(?P<stepper>[-\w]+)/edit/$', EditTestCaseView.as_view(), name='edit-testcase-stepper'),
    url(r'^testsuites/(?P<stepper>[-\w]+)/new/$', NewTestSuiteView.as_view(), name="new-testsuites-stepper"),
    url(r'^testsuites/(?P<pk>\d+)/(?P<stepper>[-\w]+)/edit/$', EditTestSuiteView.as_view(), name="edit-testsuites-stepper"),
    url(r'^(?P<pk>\d+)/(?P<type_script>\d+)/(?P<stepper>[-\w]+)/run$', RunScriptView.as_view(), name="run-script-stepper"),
]
